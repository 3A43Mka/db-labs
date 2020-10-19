from consolemenu import *
from consolemenu.items import *


class View:
    def print(self, data):
        columns, rows = data
        lineLen = 30 * len(columns)

        self.print_separator(lineLen)
        self.print_row(columns)
        self.print_separator(lineLen)

        for row in rows:
            self.print_row(row)
        self.print_separator(lineLen)

    def print_row(self, row):
        for col in row:
            print(str(col).ljust(26, ' ') + '   |', end='')
        print('')

    def print_separator(self, length):
        print('-' * length)