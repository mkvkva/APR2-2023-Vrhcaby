from tabulate import tabulate
import random


class Backgammon:
    def __init__(self):
        # игровая доска
        self.board = {1: -2, 2: 0, 3: 0, 4: 0, 5: 0, 6: 5,
                      7: 0, 8: 3, 9: 0, 10: 0, 11: 0, 12: -5,
                      13: 5, 14: 0, 15: 0, 16: 0, 17: -3, 18: 0,
                      19: -5, 20: 0, 21: 0, 22: 0, 23: 0, 24: 2
                      }
        # игровые значения
        self.dice1_value = 0  # значение первого куба
        self.dice2_value = 0  # значение второго куба
        self.dice_values_list = []  # список значений кубов

        self.first_turn = None  # кто ходит первым

        self.number_point_from = 0  # из какого пункта берем шашку
        self.number_point_to = 0  # не нужная переменная
        self.user_turn_value = 0  # какое значение игрок хочет использовать для хода

        self.bar_white_value = 0  # белые шашки на баре
        self.bar_black_value = 0  # черные шашки на баре

        self.bearing_off_white = 0  # выведенные белые шашки
        self.bearing_off_black = 0  # выведенные черные шашки

    # функция выводящая игровую доску в виде таблицы
    def print_board(self):
        point_numbers = ["Čísla poli"]
        for number in self.board.keys():
            point_numbers.append(str(number))

        point_values = ["Počet kamenů"]
        for value in self.board.values():
            point_values.append(str(value))

        print(tabulate([point_values], headers=point_numbers, tablefmt="fancy_grid"))

    # функция выводящая количество выбитых шашек
    def print_bar(self):
        print(tabulate([[self.bar_white_value, self.bar_black_value]],
                       headers=["Bílé kameny na baru", "Černé kameny na baru"],
                       tablefmt="fancy_grid"))

    # функция выводящая количество выведенных из игры шашек
    def print_bearing_off(self):
        print(tabulate([[self.bearing_off_white, self.bearing_off_black]],
                       headers=["Vyvedené bílé kameny", "Vyvedené černé kameny"],
                       tablefmt="fancy_grid"))

    # бросок кубиков
    def roll_dices(self):
        self.dice1_value = random.randint(1, 6)
        self.dice2_value = random.randint(1, 6)

        if self.dice1_value != self.dice2_value:
            self.dice_values_list.append(self.dice1_value)
            self.dice_values_list.append(self.dice2_value)
        else:
            self.dice_values_list.append(self.dice1_value)
            self.dice_values_list.append(self.dice1_value)
            self.dice_values_list.append(self.dice2_value)
            self.dice_values_list.append(self.dice2_value)
        return self.dice_values_list

    # функция определяющая кто ходит первым
    def who_is_first(self):
        is_error_turn4 = True
        values_list = []
        while is_error_turn4:
            values_list.clear()
            values_list = self.roll_dices()
            print(f"Čísla na kostkách: {self.dice1_value}, {self.dice2_value}")
            if len(self.dice_values_list) == 2:
                is_error_turn4 = False
                if self.dice1_value > self.dice2_value:
                    print("Bilé dělají první tah.")
                    print("")
                    self.first_turn = "White"
                else:
                    print("Černé dělají první tah.")
                    print("")
                    self.first_turn = "Black"
            elif len(self.dice_values_list) == 4:
                print("Na kostkách jsou stejné hodnoty. Je nutno přehodit.")
                print("")
        return self.first_turn
