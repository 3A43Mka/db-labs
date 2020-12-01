from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgres://postgres:111223@localhost:5432/lab2_test', isolation_level='SERIALIZABLE')
Base = declarative_base()


class Repr:
    def __repr__(self):
        clean_dict = self.__dict__.copy()
        clean_dict.pop('_sa_instance_state')
        return f'<{self.__class__.__name__}>{clean_dict})'


class Level(Base, Repr):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    blob = Column(String)

    players = relationship('Player')

    def __init__(self, title=None, description=None, blob=None):
        self.title = title
        self.description = description
        self.blob = blob


class Player(Base, Repr):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    last_online = Column(Date)
    health = Column(Integer)
    level_id = Column(Integer, ForeignKey('level.id'))

    player_skins = relationship("PlayerSkin")

    def __init__(self, nickname=None, last_online=None, health=None, level_id=None):
        self.nickname = nickname
        self.last_online = last_online
        self.health = health
        self.level_id = level_id


class Skin(Base, Repr):
    __tablename__ = 'skin'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    blob = Column(String)

    player_skins = relationship("PlayerSkin")

    def __init__(self, title=None, blob=None):
        self.title = title
        self.blob = blob


class PlayerSkin(Base, Repr):
    __tablename__ = 'player_skin'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    skin_id = Column(Integer, ForeignKey('skin.id'))

    def __init__(self, player_id=None, skin_id=None):
        self.player_id = player_id
        self.skin_id = skin_id


session = sessionmaker(engine)()
Base.metadata.create_all(engine)

TABLES = {'level': Level, 'player': Player, 'skin': Skin, 'player_skin': PlayerSkin}


class Model:
    def pairs_from_str(self, string):
        lines = string.split(',')
        pairs = {}
        for line in lines:
            key, value = line.split('=')
            pairs[key.strip()] = value.strip()
        return pairs

    def filter_by_pairs(self, objects, pairs, cls):
        for key, value in pairs.items():
            field = getattr(cls, key)
            objects = objects.filter(field == value)
        return objects

    def get(self, table_name, condition):

        object_class = TABLES[table_name]
        objects = session.query(object_class)

        if condition:
            try:
                pairs = self.pairs_from_str(condition)
            except Exception as err:
                raise Exception('Incorrect input')
            objects = self.filter_by_pairs(objects, pairs, object_class)

        return list(objects)

    def insert(self, table_name, columns, values):
        columns = [c.strip() for c in columns.split(',')]
        values = [v.strip() for v in values.split(',')]

        pairs = dict(zip(columns, values))
        object_class = TABLES[table_name]
        obj = object_class(**pairs)

        session.add(obj)

    def commit(self):
        session.commit()

    def delete(self, table_name, condition):
        try:
            pairs = self.pairs_from_str(condition)
        except Exception as err:
            raise Exception('Incorrect input')
        object_class = TABLES[table_name]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        objects.delete()

    def update(self, table_name, condition, statement):
        try:
            pairs = self.pairs_from_str(condition)
            new_values = self.pairs_from_str(statement)
        except Exception as err:
            raise Exception('Incorrect input')

        object_class = TABLES[table_name]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        for obj in objects:
            for field_name, value in new_values.items():
                setattr(obj, field_name, value)

    def fill_level_by_random_data(self, quantity):
        sql = f'''
        CREATE OR REPLACE FUNCTION randomLevels()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step > {quantity};
                INSERT INTO level (title, description, blob)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    substring(md5(random()::text), 1, 15),
                    substring(md5(random()::text), 1, 15)
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomLevels();
        '''
        try:
            session.execute(sql)
        finally:
            session.commit()
