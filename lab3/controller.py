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


def get_input(msg, tableName=''):
    print(msg)
    if tableName:
        print(' , '.join(TABLES[tableName]), end='\n\n')
    return input()


def get_insert_input(msg, tableName):
    print(msg)
    print(' , '.join(TABLES[tableName]), end='\n\n')
    return input(), input()


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_init_menu(self, message=''):
        selection_menu = SelectionMenu(
            TABLES_NAMES + ['Fill table "level" by random data', 'Commit'], title='Menu:', subtitle=message)
        selection_menu.show()

        index = selection_menu.selected_option
        if index < len(TABLES_NAMES):
            tableName = TABLES_NAMES[index]
            self.show_entity_menu(tableName)
        elif index == len(TABLES_NAMES):
            self.fill_level_by_random_data()
        elif index == len(TABLES_NAMES) + 1:
            self.model.commit()
            self.show_init_menu(message='Commit success')
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
            self.show_init_menu()

    def get(self, table_name):
        try:
            condition = get_input(
                f'GET {table_name}\nEnter search criteria:', table_name)
            data = self.model.get(table_name, condition)
            self.view.print_entities(table_name, data)
            input()
            self.show_entity_menu(table_name)
        except Exception:
            self.show_entity_menu(table_name, 'Invalid search criteria')

    def insert(self, table_name):
        try:
            columns, values = get_insert_input(
                f"INSERT {table_name}\nEnter columns, then values", table_name)
            self.model.insert(table_name, columns, values)
            self.show_entity_menu(table_name, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(table_name, 'Invalid insert arguments')

    def delete(self, table_name):
        try:
            condition = get_input(
                f'DELETE {table_name}\n Enter criteria for deletion:', table_name)
            self.model.delete(table_name, condition)
            self.show_entity_menu(table_name, 'Delete is successful')
        except Exception:
            self.show_entity_menu(table_name, 'Invalid deleting criteria')

    def update(self, tableName):
        try:
            condition = get_input(
                f'UPDATE {tableName}\nEnter criteria:', tableName)
            statement = get_input(
                "Enter columns and their new values", tableName)
            self.model.update(tableName, condition, statement)
            self.show_entity_menu(tableName, 'Update is successful')
        except Exception:
            self.show_entity_menu(tableName, 'Invalid update values')

    def fill_level_by_random_data(self):
        try:
            quantity = get_input('Enter quantity:')
            self.model.fill_level_by_random_data(quantity)
            self.show_init_menu('Generated successfully')

        except Exception:
            self.show_init_menu('Invalid quantity')