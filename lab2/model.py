import psycopg2


class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost",
                                               database='lab2_test', user='postgres', password='111223')
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error):
            print("Error connecting to server")

    def get_col_names(self):
        return [d[0] for d in self.cursor.description]

    def get(self, tname, condition):
        try:
            query = f'SELECT * FROM {tname}'
            if condition:
                query += ' WHERE ' + condition
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def insert(self, tname, columns, values):
        try:
            query = f'INSERT INTO {tname} ({columns}) VALUES ({values});'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def delete(self, tname, condition):
        try:
            query = f'DELETE FROM {tname} WHERE {condition};'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def update(self, tname, condition, statement):
        try:
            query = f'UPDATE {tname} SET {statement} WHERE {condition}'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def search_players_on_level_by_levelname_health_nickname(self, levelname, a, b, nickname):
        try:
            query = f'''
            SELECT player.id, player.nickname, player.last_online, player.health
            FROM level INNER JOIN player ON level.id = player.level_id
            WHERE LOWER(player.nickname) Like '%{nickname.lower()}%' AND LOWER(level.title) Like '%{levelname.lower()}%' AND player.health Between {a} And {b}
            '''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def search_skin_by_playerhealth_online_levelname(self, a, b, date1, date2, levelname):
        try:
            query = f'''
            SELECT skin.id, skin.title, skin.blob
            FROM skin INNER JOIN level INNER JOIN player ON level.id = player.level_id 
            INNER JOIN player_skin ON player.id = player_skin.player_id ON skin.id = player_skin.skin_id
            WHERE player.last_online Between '{date1}' And '{date2}' 
            AND player.health Between {a} And {b} AND LOWER(level.title) Like '%{levelname.lower()}%' GROUP BY skin.id
            '''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def count_players_with_skin_by_skin_name_levelname_health(self, skintitle, levelname, a, b):
        try:
            query = f'''
            SELECT COUNT (*)
            FROM skin INNER JOIN level INNER JOIN player ON level.id = player.level_id INNER JOIN player_skin ON player.id = player_skin.player_id ON skin.id = player_skin.skin_id
            WHERE LOWER(skin.title) Like '%{skintitle.lower()}%' AND LOWER(level.title) Like '%{levelname.lower()}%' AND player.health Between {a} And {b}
            GROUP BY skin.title
            '''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

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
            self.cursor.execute(sql)
        finally:
            self.connection.commit()
