from consolemenu import SelectionMenu
import time

from model import Model
from view import View


TABLES_NAMES = ['level', 'player', 'skin', 'player_skin']
TABLES = {
    'level': ['id', 'title', 'description', 'blob'],
    'player': ['id', 'nickname', 'last_online', 'health', 'level_id'],
    'skin': ['id', 'title', 'blob'],
    'player_skin': ['id', 'player_id', 'skin_id']
}


def getInput(msg, tableName=''):
    print(msg)
    if tableName:
        print(' , '.join(TABLES[tableName]), end='\n\n')
    return input()


def getInsertInput(msg, tableName):
    print(msg)
    print(' , '.join(TABLES[tableName]), end='\n\n')
    return input(), input()


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run_menu(self, message=''):
        selectionMenu = SelectionMenu(
            TABLES_NAMES + ['Search players by level name with set health and nickname',
                            'Find skins by player health, last online and level',
                            'Count players who own skin by skin name, level title and health',
                            'Fill table "level" by random data'], title='Menu:', subtitle=message)
        selectionMenu.show()

        index = selectionMenu.selected_option
        if index < len(TABLES_NAMES):
            tableName = TABLES_NAMES[index]
            self.show_entity_menu(tableName)
        elif index == 4:
            self.search_players_on_level_by_levelname_health_nickname()
        elif index == 5:
            self.search_skin_by_playerhealth_online_levelname()
        elif index == 6:
            self.count_players_with_skin_by_skin_name_levelname_health()
        elif index == 7:
            self.fill_level_by_random_data()
        else:
            print('Closing...')

    def show_entity_menu(self, tableName, msg=''):
        options = ['Get',  'Delete', 'Update', 'Insert']
        functions = [self.get, self.delete, self.update, self.insert]

        selectionMenu = SelectionMenu(options, f'{tableName}',
                                      exit_option_text='Back', subtitle=msg)
        selectionMenu.show()
        try:
            function = functions[selectionMenu.selected_option]
            function(tableName)
        except IndexError:
            self.run_menu()

    def get(self, tableName):
        try:
            condition = getInput(
                f'GET {tableName}\nEnter search criteria:', tableName)
            start_time = time.time()
            data = self.model.get(tableName, condition)
            self.view.print(data)
            print("\nQuery time:", time.time() - start_time)
            input()
            self.show_entity_menu(tableName)
        except Exception:
            self.show_entity_menu(tableName, 'Invalid search criteria')

    def insert(self, tableName):
        try:
            columns, values = getInsertInput(
                f"INSERT {tableName}\nEnter columns, then values", tableName)
            self.model.insert(tableName, columns, values)
            self.show_entity_menu(tableName, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(tableName, 'Invalid insert arguments')

    def delete(self, tableName):
        try:
            condition = getInput(
                f'DELETE {tableName}\n Enter criteria for deletion:', tableName)
            self.model.delete(tableName, condition)
            self.show_entity_menu(tableName, 'Delete is successful')
        except Exception:
            self.show_entity_menu(tableName, 'Invalid deleting criteria')

    def update(self, tableName):
        try:
            condition = getInput(
                f'UPDATE {tableName}\nEnter criteria:', tableName)
            statement = getInput(
                "Enter columns and their new values", tableName)
            self.model.update(tableName, condition, statement)
            self.show_entity_menu(tableName, 'Update is successful')
        except Exception:
            self.show_entity_menu(tableName, 'Invalid update values')

    def search_players_on_level_by_levelname_health_nickname(self):
        try:
            levelname = getInput('Enter level name')
            a = getInput('Enter min health')
            b = getInput('Enter max health')
            nickname = getInput('Enter nickname')
            start_time = time.time()
            data = self.model.search_players_on_level_by_levelname_health_nickname(levelname, a, b, nickname)
            self.view.print(data)
            print("\nQuery time:", time.time() - start_time)
            input()
            self.run_menu()
        except Exception:
            self.run_menu('Invalid search arguments')

    def search_skin_by_playerhealth_online_levelname(self):
        try:
            minhealth = getInput('Enter minimum health')
            maxhealth = getInput('Enter max health')
            mindate = getInput('Enter min date player was online')
            maxdate = getInput('Enter max date player was online')
            levelname = getInput('Enter level name')
            start_time = time.time()
            data = self.model.search_skin_by_playerhealth_online_levelname(minhealth, maxhealth, mindate, maxdate, levelname)
            self.view.print(data)
            print("\nQuery time:", time.time() - start_time)
            input()
            self.run_menu()
        except Exception:
            self.run_menu('Invalid search arguments')

    def count_players_with_skin_by_skin_name_levelname_health(self):
        try:
            skintitle = getInput('Enter skin title')
            levelname = getInput('Enter level name')
            minhealth = getInput('Enter min player health')
            maxhealth = getInput('Enter max player health')
            start_time = time.time()
            data = self.model.count_players_with_skin_by_skin_name_levelname_health(skintitle, levelname, minhealth, maxhealth)
            self.view.print(data)
            print("\nQuery time:", time.time() - start_time)
            input()
            self.run_menu()
        except Exception:
            self.run_menu('Invalid search arguments')

    def fill_level_by_random_data(self):
        try:
            quantity = getInput('Enter quantity:')
            self.model.fill_level_by_random_data(quantity)
            self.run_menu('Generated successfully')

        except Exception:
            self.run_menu('Invalid quantity')