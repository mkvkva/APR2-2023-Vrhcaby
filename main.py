from tabulate import tabulate
from colorama import init

import random
import json


class Backgammon:
    def __init__(self):
        # игровая доска
        self.board = {1: -2, 2: 0, 3: 0, 4: 0, 5: 0, 6: 5,
                      7: 0, 8: 3, 9: 0, 10: 0, 11: 0, 12: -5,
                      13: 5, 14: 0, 15: 0, 16: 0, 17: -3, 18: 0,
                      19: -5, 20: 0, 21: 0, 22: 0, 23: 0, 24: 2
                      }
        # игровые  значения
        self.dice1_value = 0
        self.dice2_value = 0
        self.dice_values_list = []

        self.first_turn = None

        self.number_point_from = 0
        self.user_turn_value = 0

        self.bar_white_value = 0
        self.bar_black_value = 0

        self.bearing_off_white = 0
        self.bearing_off_black = 0

        self.home_is_full = None
        self.possible_turns_allow_kost = []
        self.possible_turns_allow_pole = []
        self.datas_ai_good = []  # Массив содержащий набор предыдущих историй ходов выигранных AI
        self.datas_ai_bad = []  # Массив содержащий набор предыдущих историй ходов проигранных AI
        self.history_game = []  # Массив содержащий текущую историю ходов игроков

    def print_board(self):
        print("Hrací pole:")
        point_numbers_up = []
        point_values_up = []
        point_numbers_down = []
        point_values_down = []

        for key, value in self.board.items():
            if key >= 13:
                point_numbers_up.append(str(key))
                if value == 0:
                    point_values_up.append("  ")
                if (abs(value) > 0) and (abs(value) < 10):
                    if (value < 0) or (abs(value) > 9):
                        point_values_up.append(str(value))
                    else:
                        point_values_up.append(str(value) + " ")
                if abs(value) > 9:
                    point_values_up.append(str(value))

            if key < 10:
                point_numbers_down.append(str(key) + " ")
                if value == 0:
                    point_values_down.append("  ")
                if (abs(value) > 0) and (abs(value) < 10):
                    if (value < 0) or (abs(value) > 9):
                        point_values_down.append(str(value))
                    else:
                        point_values_down.append(str(value) + " ")
                if abs(value) > 9:
                    point_values_down.append(str(value))

            if (key < 13) and (key >= 10):
                point_numbers_down.append(str(key))
                if value == 0:
                    point_values_down.append("  ")
                else:
                    point_values_down.append(str(value))

        # Переставляем зеркально числа в нижней части игрового поля

        point_numbers_down_mirror = [' '] * len(point_numbers_down)
        point_values_down_mirror = [' '] * len(point_numbers_down)

        position = len(point_numbers_down)

        for i in point_numbers_down:
            position -= 1
            point_numbers_down_mirror[position] = i

        position = len(point_values_down)
        for i in point_values_down:
            position -= 1
            point_values_down_mirror[position] = i

        table = point_numbers_up, point_values_up, ["  "] * len(
            point_values_down), point_values_down_mirror, point_numbers_down_mirror
        print(tabulate(table, tablefmt="fancy_grid"))

    # функция выводящая количество выбитых шашек и шашек в баре
    def print_bar_bearing_off(self):
        if self.bar_white_value or self.bearing_off_white or self.bar_black_value or self.bearing_off_black:
            color_tabl = "blue"
        else:
            color_tabl = "white"

        headers = ["Kamen", "Na baru", "Vyvedené"]
        table = ["Bílé", str(self.bar_white_value), str(self.bearing_off_white)], \
            ["Černé", str(self.bar_black_value), str(self.bearing_off_black)]
        printc(tabulate(table, headers, tablefmt="fancy_grid"), color_tabl)

    # бросок кубиков
    def roll_dices(self):
        self.dice_values_list = []
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

    # Найдем и покажем допустимые ходы для белых шашек
    def legal_moves_white(self):
        while self.dice_values_list:

            if self.bar_white_value == 0:  # Если нет белых шашек отправленных в бар
                # Проверка: можно ли сделать хоть один ход белыми шашками

                for key in self.board.keys():
                    if 7 <= key <= 24:
                        if self.board[key] > 0:
                            self.home_is_full = False  # Дом белых еще не заполнен
                            break
                        else:
                            self.home_is_full = True  # В доме белых все шашки

                possible_turns = []
                self.possible_turns_allow_kost = []
                self.possible_turns_allow_pole = []

                for value in self.dice_values_list:
                    for key in self.board.keys():
                        if self.board[key] > 0:  # Перебираем на доске только позиции белых

                            try:
                                if self.board[key - value] <= -2:  # Если позиция занята двумя и более черными шашками
                                    possible_turns.append(0)
                                else:
                                    possible_turns.append(1)
                                    self.possible_turns_allow_kost.append(value)
                                    self.possible_turns_allow_pole.append(key)

                            except KeyError:
                                if self.home_is_full:
                                    possible_turns.append(1)
                                    self.possible_turns_allow_kost.append(value)
                                    self.possible_turns_allow_pole.append(key)

                                else:
                                    possible_turns.append(0)

                if 1 in possible_turns:
                    printc("Možné pohyby bílých:", "yellow")
                    printc(
                        tabulate([["Kost"] + self.possible_turns_allow_kost],
                                 headers=["Číslo poli"] + self.possible_turns_allow_pole,
                                 tablefmt="fancy_grid"), "white")

                    break
                else:
                    if backgammon.bearing_off_white != 15:
                        printc("\nNení možné udělat žádný tah.", "red")
                        self.dice_values_list = []  # Обнуляем значения выпавших костей
                        break
                    else:
                        self.dice_values_list = []  # Обнуляем значения выпавших костей
                        break

            else:
                # ситуация когда игрок должен ввести свою побитую шашку в игру
                if self.bar_white_value:

                    # код проверяющий можно ли сделать ход
                    possible_turns = []
                    self.possible_turns_allow_kost = []
                    self.possible_turns_allow_pole = []

                    for value in self.dice_values_list:
                        for i in range(self.bar_white_value):

                            if self.board[25 - value] <= -2:
                                possible_turns.append(0)
                            else:
                                possible_turns.append(1)
                                self.possible_turns_allow_kost.append(value)
                                self.possible_turns_allow_pole.append(25 - value)

                    if 1 in possible_turns:

                        printc("Možné pohyby bílých:", "yellow")
                        printc(
                            tabulate([["Kost"] + self.possible_turns_allow_kost],
                                     headers=["Číslo poli"] + self.possible_turns_allow_pole,
                                     tablefmt="fancy_grid"), "red")
                        break

                    else:
                        printc("\nNení možné uvést kamen na desku.", "red")
                        self.dice_values_list = []
                        break

    # Найдем и покажем допустимые ходы для черных шашек
    def legal_moves_black(self):
        while self.dice_values_list:

            if self.bar_black_value == 0:

                for key in self.board.keys():
                    if 1 <= key <= 18:
                        if self.board[key] < 0:
                            self.home_is_full = False
                            break
                        else:
                            self.home_is_full = True

                possible_turns = []
                self.possible_turns_allow_kost = []
                self.possible_turns_allow_pole = []

                for value in self.dice_values_list:
                    for key in self.board.keys():
                        if self.board[key] < 0:

                            try:
                                if self.board[key + value] >= 2:
                                    possible_turns.append(0)
                                else:
                                    possible_turns.append(1)
                                    self.possible_turns_allow_kost.append(value)
                                    self.possible_turns_allow_pole.append(key)
                            except KeyError:
                                if self.home_is_full:
                                    possible_turns.append(1)
                                    self.possible_turns_allow_kost.append(value)
                                    self.possible_turns_allow_pole.append(key)
                                else:
                                    possible_turns.append(0)

                if 1 in possible_turns:
                    printc("Možné pohyby černých:", "yellow")
                    printc(
                        tabulate([self.possible_turns_allow_kost], headers=self.possible_turns_allow_pole,
                                 tablefmt="fancy_grid"), "white")
                    break

                else:
                    if backgammon.bearing_off_black != 15:
                        printc("\nNení možné udělat žádný tah.", "red")
                        self.dice_values_list = []
                        break
                    else:
                        self.dice_values_list = []
                        break

            else:
                if self.bar_black_value:

                    possible_turns = []
                    self.possible_turns_allow_kost = []
                    self.possible_turns_allow_pole = []

                    for value in self.dice_values_list:
                        for i in range(self.bar_black_value):

                            if self.board[value] >= 2:
                                possible_turns.append(0)
                            else:
                                possible_turns.append(1)
                                self.possible_turns_allow_kost.append(value)
                                self.possible_turns_allow_pole.append(value)

                    if 1 in possible_turns:

                        printc("Možné pohyby černých:", "yellow")
                        printc(tabulate([self.possible_turns_allow_kost], headers=self.possible_turns_allow_pole,
                                        tablefmt="fancy_grid"), "red")
                        break
                    else:
                        printc("\nNení možné uvést kamen na desku.", "red")
                        self.dice_values_list = []
                        break

    # Найдем допустимые ходы для AI
    def legal_moves_black_ai(self):
        while self.dice_values_list:

            if self.bar_black_value == 0:
                for key in self.board.keys():
                    if 1 <= key <= 18:
                        if self.board[key] < 0:
                            self.home_is_full = False
                            break
                        else:
                            self.home_is_full = True

                possible_turns = []
                self.possible_turns_allow_kost = []
                self.possible_turns_allow_pole = []

                for value in self.dice_values_list:
                    for key in self.board.keys():
                        if self.board[key] < 0:

                            try:
                                if self.board[key + value] >= 2:
                                    possible_turns.append(0)
                                else:
                                    possible_turns.append(1)
                                    self.possible_turns_allow_kost.append(value)
                                    self.possible_turns_allow_pole.append(key)
                            except KeyError:
                                if self.home_is_full:
                                    possible_turns.append(1)
                                    self.possible_turns_allow_kost.append(value)
                                    self.possible_turns_allow_pole.append(key)
                                else:
                                    possible_turns.append(0)
                if 1 in possible_turns:
                    break
                else:
                    if backgammon.bearing_off_black != 15:
                        printc("\nAI: Není možné udělat žádný tah.", "red")
                        print(self.dice_values_list)
                        print(self.possible_turns_allow_pole)
                        print(self.possible_turns_allow_kost)
                        self.dice_values_list = []
                        break
                    else:
                        self.dice_values_list = []
                        break

            else:
                if self.bar_black_value:

                    possible_turns = []
                    self.possible_turns_allow_kost = []
                    self.possible_turns_allow_pole = []

                    for value in self.dice_values_list:
                        for i in range(self.bar_black_value):

                            if self.board[value] >= 2:
                                possible_turns.append(0)
                            else:
                                possible_turns.append(1)
                                self.possible_turns_allow_kost.append(value)
                                self.possible_turns_allow_pole.append(value)

                    if 1 in possible_turns:
                        break
                    else:
                        printc("\nAI: Není možné uvést kamen na desku.", "red")
                        print(self.dice_values_list)
                        print(self.possible_turns_allow_pole)
                        print(self.possible_turns_allow_kost)

                        self.dice_values_list = []
                        break

    # функция определяющая кто ходит первым
    def who_is_first(self):
        is_error_turn4 = True
        values_list = []
        while is_error_turn4:
            values_list.clear()
            values_list = self.roll_dices()
            printc(f"Čísla na kostkách: {self.dice1_value}, {self.dice2_value}", "green")
            if len(self.dice_values_list) == 2:
                is_error_turn4 = False
                if self.dice1_value > self.dice2_value:
                    printc("Bilé dělají první tah.", "yellow")
                    print("")
                    self.first_turn = "White"
                else:
                    printc("Černé dělají první tah.", "yellow")
                    print("")
                    self.first_turn = "Black"
            elif len(self.dice_values_list) == 4:
                printc("Na kostkách jsou stejné hodnoty. Je nutno přehodit.", "red")
                print("")
        return self.first_turn

    # основная игровая функция, реализующая ход белых шашек
    def white_turn(self):
        is_error_turn1 = True
        is_error_turn2 = True
        self.home_is_full = None

        while self.dice_values_list:
            printc(
                "------------------------------------------------------------\n                   TAH (BÍLÝCH)                    "
                "\n------------------------------------------------------------", "violet")
            printc(f"Čísla na kostkách: {self.dice1_value}, {self.dice2_value}", "green")
            self.print_board()
            self.print_bar_bearing_off()

            if len(self.dice_values_list) == 0:
                break

            if backgammon.bearing_off_white == 15:
                break

            self.legal_moves_white()  # Вывод допустимых ходов белыми шашками

            if len(self.dice_values_list) == 0:
                break

            if backgammon.bearing_off_white == 15:
                break

            is_error_turn3 = True

            if self.bar_white_value == 0:

                # просим от игрока ввести номер пункта с которого он хочет снять шашку
                while is_error_turn1:
                    is_error_turn2 = True

                    self.number_point_from = input("\nZadejte číslo poli ze kterého chcete posunout kamen: ")
                    if self.number_point_from.isnumeric():
                        self.number_point_from = int(self.number_point_from)
                        if 1 <= self.number_point_from <= 24:

                            for key in self.board.keys():
                                if key == self.number_point_from:
                                    if self.board[self.number_point_from] > 0:

                                        is_error_turn1 = False

                                    else:
                                        printc("Na daném poli není žádného vašého kamenu.", "red")

                        else:
                            printc("Zadejte číslo od 1 do 24.", "red")
                    else:
                        printc("Zadejte číslo od 1 do 24.", "red")

                # просим от игрока ввести значение, соответствущее значениям на кубиках,
                # на которое он хочет передвинуть шашку
                while is_error_turn2:
                    is_error_turn1 = True

                    self.user_turn_value = input("\nZadejte hodnotu svého tahu podle kostky: ")
                    if self.user_turn_value.isnumeric():
                        self.user_turn_value = int(self.user_turn_value)
                        if self.user_turn_value in self.dice_values_list:
                            is_error_turn2 = False

                            # здесь выбираются возможности, которые могут произойти с шашкой
                            # либо шашку переместить не удастся, либо она побьет шашку противника,
                            # либо просто переместиться на новый пункт
                            # либо её удастся вывести из игры, если все шашки игрока будут находиться в доме
                            try:
                                if self.board[self.number_point_from - self.user_turn_value] <= -2:
                                    is_error_turn2 = True
                                    printc("Nelze přesunout kamen, pole je obsazeno oponentem.", "red")
                                    break
                                elif self.board[self.number_point_from - self.user_turn_value] == -1:
                                    self.board[self.number_point_from] -= 1
                                    self.board[self.number_point_from - self.user_turn_value] += 2
                                    self.dice_values_list.remove(self.user_turn_value)
                                    self.bar_black_value += 1
                                    printc("Kamen oponenta byl vyhozen.", "red")
                                    # запишем в историю ход белых
                                    self.history_game.append(self.number_point_from)  # Запоминаем выбраную позицию
                                    self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                                else:
                                    self.board[self.number_point_from] -= 1
                                    self.board[self.number_point_from - self.user_turn_value] += 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    printc("Kamen byl přesunen.", "yellow")
                                    # запишем в историю ход белых
                                    self.history_game.append(self.number_point_from)  # Запоминаем выбраную позицию
                                    self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень

                            except KeyError:

                                if self.home_is_full:
                                    self.board[self.number_point_from] -= 1
                                    self.bearing_off_white += 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    printc("Kamen byl vyveden.", "blue")
                                    # запишем в историю этот ход белых
                                    self.history_game.append(self.number_point_from)  # Запоминаем выбраную позицию
                                    self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                                else:
                                    is_error_turn2 = True
                                    printc("Nemůžete vyvest kamen pokud nemáte je všech doma.", "red")
                                    break

                        else:
                            print("Zadejte číslo podle kostky.")
                    else:
                        print("Zadejte číslo podle kostky.")

            else:
                # ситуация когда игрок должен ввести свою побитую шашку в игру
                if self.bar_white_value:

                    # код проверяющий можно ли сделать ход
                    possible_turns = []
                    for value in self.dice_values_list:
                        for i in range(self.bar_white_value):

                            if self.board[25 - value] <= -2:
                                possible_turns.append(0)
                            else:
                                possible_turns.append(1)

                    if 1 in possible_turns:

                        # здесь игрок вводит номер пункта, куда хочет ввести шашку
                        while is_error_turn3:

                            printc("\nMusíte vyvest kamen z baru.", "red")
                            self.user_turn_value = input("Zadejte hodnotu svého tahu podle kostky: ")
                            if self.user_turn_value.isnumeric():
                                self.user_turn_value = int(self.user_turn_value)
                                if self.user_turn_value in self.dice_values_list:

                                    if self.board[25 - self.user_turn_value] <= -2:
                                        printc("Nelze přesunout kamen, pole je obsazeno oponentem.", "red")
                                    elif self.board[25 - self.user_turn_value] == -1:
                                        is_error_turn3 = False
                                        self.bar_white_value -= 1
                                        self.board[25 - self.user_turn_value] += 2
                                        self.dice_values_list.remove(self.user_turn_value)
                                        self.bar_black_value += 1
                                        printc("Kamen oponenta byl vyhozen.", "red")
                                        # запишем в историю этот ход белых
                                        self.history_game.append(
                                            25 - self.user_turn_value)  # Запоминаем выбраную позицию
                                        self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                                    else:
                                        is_error_turn3 = False
                                        self.bar_white_value -= 1
                                        self.board[25 - self.user_turn_value] += 1
                                        self.dice_values_list.remove(self.user_turn_value)
                                        print("Kamen byl přesunen.")
                                        self.history_game.append(
                                            25 - self.user_turn_value)  # Запоминаем выбраную позицию
                                        self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень

                                else:
                                    printc("Zadejte číslo podle kostky.", "red")
                            else:
                                printc("Zadejte číslo podle kostky.", "red")

                    else:
                        printc("\nNení možno uvést kamen na desku.", "red")
                        self.dice_values_list = []
                        break

    # аналогичная функция для реализации хода, но уже для черных шашек
    def black_turn(self):
        printc(
            "------------------------------------------------------------\n                   TAH (ČERNÝCH)                    "
            "\n------------------------------------------------------------", "violet")

        is_error_turn1 = True
        is_error_turn2 = True
        self.home_is_full = None

        printc(f"Čísla na kostkách: {self.dice1_value}, {self.dice2_value}", "green")

        while self.dice_values_list:

            self.print_board()
            backgammon.print_bar_bearing_off()

            if len(self.dice_values_list) == 0:
                break

            if backgammon.bearing_off_black == 15:
                break

            self.legal_moves_black()

            is_error_turn3 = True

            if self.bar_black_value == 0:

                while is_error_turn1:
                    is_error_turn2 = True

                    self.number_point_from = input("\nZadejte číslo poli ze kterého chcete posunout kamen: ")
                    if self.number_point_from.isnumeric():
                        self.number_point_from = int(self.number_point_from)
                        if 1 <= self.number_point_from <= 24:

                            for key in self.board.keys():
                                if key == self.number_point_from:
                                    if self.board[self.number_point_from] < 0:

                                        is_error_turn1 = False

                                    else:
                                        print("Na daném poli není žádného vašého kamenu.")

                        else:
                            print("Zadejte číslo od 1 do 24.")
                    else:
                        print("Zadejte číslo od 1 do 24.")

                while is_error_turn2:
                    is_error_turn1 = True

                    self.user_turn_value = input("\nZadejte hodnotu svého tahu podle kostky: ")
                    if self.user_turn_value.isnumeric():
                        self.user_turn_value = int(self.user_turn_value)
                        if self.user_turn_value in self.dice_values_list:
                            is_error_turn2 = False

                            try:
                                if self.board[self.number_point_from + self.user_turn_value] >= 2:
                                    is_error_turn2 = True
                                    print("Nelze přesunout kamen, pole je obsazeno oponentem.")
                                    break
                                elif self.board[self.number_point_from + self.user_turn_value] == 1:
                                    self.board[self.number_point_from] += 1
                                    self.board[self.number_point_from + self.user_turn_value] -= 2
                                    self.dice_values_list.remove(self.user_turn_value)
                                    self.bar_white_value += 1
                                    print("Kamen oponenta byl vyhozen.")
                                    # запишем в историю этот ход черных
                                    self.history_game.append(-self.number_point_from)  # Запоминаем выбраную позицию
                                    self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                                else:
                                    self.board[self.number_point_from] += 1
                                    self.board[self.number_point_from + self.user_turn_value] -= 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    print("Kamen byl přesunen.")
                                    # запишем в историю этот ход черных
                                    self.history_game.append(-self.number_point_from)  # Запоминаем выбраную позицию
                                    self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень

                            except KeyError:

                                if self.home_is_full:
                                    self.board[self.number_point_from] += 1
                                    self.bearing_off_black += 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    print("Kamen byl vyveden.")
                                    # запишем в историю этот ход черных
                                    self.history_game.append(-self.number_point_from)  # Запоминаем выбраную позицию
                                    self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                                else:
                                    is_error_turn2 = True
                                    print("Nemůžete vyvest kamen pokud nemáte je všech doma.")
                                    break

                        else:
                            print("Zadejte číslo podle kostky.")
                    else:
                        print("Zadejte číslo podle kostky.")

            else:
                if self.bar_black_value:

                    possible_turns = []
                    for value in self.dice_values_list:
                        for i in range(self.bar_black_value):

                            if self.board[value] >= 2:
                                possible_turns.append(0)
                            else:
                                possible_turns.append(1)

                    if 1 in possible_turns:

                        while is_error_turn3:

                            print("\nMusíte vyvest kamen z baru.", end=" ")
                            self.user_turn_value = input("Zadejte hodnotu svého tahu podle kostky: ")
                            if self.user_turn_value.isnumeric():
                                self.user_turn_value = int(self.user_turn_value)
                                if self.user_turn_value in self.dice_values_list:

                                    if self.board[self.user_turn_value] >= 2:
                                        print("Nelze přesunout kamen, pole je obsazeno oponentem.")
                                    elif self.board[self.user_turn_value] == 1:
                                        is_error_turn3 = False
                                        self.bar_black_value -= 1
                                        self.board[self.user_turn_value] -= 2
                                        self.dice_values_list.remove(self.user_turn_value)
                                        self.bar_white_value += 1
                                        print("Kamen oponenta byl vyhozen.")
                                        # запишем в историю этот ход черных
                                        self.history_game.append(-self.user_turn_value)  # Запоминаем выбраную позицию
                                        self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                                    else:
                                        is_error_turn3 = False
                                        self.bar_black_value -= 1
                                        self.board[self.user_turn_value] -= 1
                                        self.dice_values_list.remove(self.user_turn_value)
                                        print("Kamen byl přesunen.")
                                        # запишем в историю этот ход черных
                                        self.history_game.append(-self.user_turn_value)  # Запоминаем выбраную позицию
                                        self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень

                                else:
                                    print("Zadejte číslo podle kostky.")
                            else:
                                print("Zadejte číslo podle kostky.")

                    else:
                        print("\nNení možno uvést kamen na desku.")

                        self.dice_values_list = []
                        break

    # AI выбирает ход
    def ai_tag(self):

        # AI ищет хороший ход
        next_gra = False
        tag_found = False
        step_gra = 0
        count_ai = 0
        while (count_ai < len(self.datas_ai_good)) and not tag_found:
            if next_gra:
                if (self.datas_ai_good[count_ai] == -99) or (self.datas_ai_good[count_ai] == 99):
                    next_gra = False
            else:
                for h in self.history_game:
                    if h != self.datas_ai_good[count_ai]:
                        next_gra = True
                        break
                    else:
                        step_gra += 1

                # Ищем полное совпадение текущих ходов AI с историей хороших ходов
                if step_gra == len(self.history_game) - 1:
                    count_pos_kost = 0
                    while count_pos_kost <= (len(self.possible_turns_allow_kost) - 1):
                        if self.datas_ai_good[count_ai + 2] == self.possible_turns_allow_kost[count_pos_kost]:
                            self.user_turn_value = self.possible_turns_allow_kost[count_pos_kost]
                            # Проверим разрешена ли позиция для выбранной кости
                            if self.datas_ai_good[count_ai + 1] == self.possible_turns_allow_pole[count_pos_kost]:
                                self.number_point_from = self.possible_turns_allow_pole[count_pos_kost]
                                tag_found = True
                                print("SHODUJE S HISTORIÍ DOBRÝCH VOLEB")
                                print(self.history_game)
                                print(self.possible_turns_allow_pole)
                                print(self.possible_turns_allow_kost)
                                print(self.number_point_from)
                                print(self.user_turn_value)
                                break
                        count_pos_kost += 1

            step_gra = 0
            count_ai += 1

        next_gra = False
        step_gra = 0
        count_ai = 0

        if not tag_found:

            # AI ищет плохой ход, чтобы исключить его использование
            while (count_ai < len(self.datas_ai_bad)) and not tag_found:
                if next_gra:
                    if (self.datas_ai_bad[count_ai] == -99) or (self.datas_ai_bad[count_ai] == 99):
                        next_gra = False
                else:
                    for h in self.history_game:
                        if h != self.datas_ai_bad[count_ai]:
                            next_gra = True
                            break
                        else:
                            step_gra += 1

                    # Полное совпадение текущих ходов с историей плохих ходов
                    if step_gra == len(self.history_game) - 1:
                        count_pos_kost = 0
                        while count_pos_kost <= (len(self.possible_turns_allow_kost) - 1):
                            if self.datas_ai_bad[count_ai + 2] != self.possible_turns_allow_kost[count_pos_kost]:
                                self.user_turn_value = self.possible_turns_allow_kost[count_pos_kost]
                                # Проверим разрешена ли позиция для выбранной кости
                                if self.datas_ai_bad[count_ai + 1] == self.possible_turns_allow_pole[count_pos_kost]:
                                    self.number_point_from = self.possible_turns_allow_pole[count_pos_kost]
                                    tag_found = True

                                    print("SHODUJE S HISTORIÍ ŠPATNÝCH VOLEB")
                                    print(self.history_game)
                                    print(self.possible_turns_allow_pole)
                                    print(self.possible_turns_allow_kost)
                                    print(self.number_point_from)
                                    print(self.user_turn_value)

                                    break
                            count_pos_kost += 1

                step_gra = 0
                count_ai += 1

        if not tag_found:
            if len(self.possible_turns_allow_pole) > 0:
                printc("AI: Nevím jak chodit, zvolím náhodný pohyb!", "turquoise")
                self.number_point_from = self.possible_turns_allow_pole[0]
                self.user_turn_value = self.possible_turns_allow_kost[0]
        else:
            printc("AI: Byl nalezen dobrý tah! (0)", "green")
            print(self.possible_turns_allow_pole)
            print(self.possible_turns_allow_kost)
            print(self.number_point_from)
            print(self.user_turn_value)

    # Ходы AI
    def ai_turn(self):
        printc(
            "------------------------------------------------------------\n                   TAH AI (ČERNÝCH)                    "
            "\n------------------------------------------------------------", "violet")

        is_error_turn1 = True
        is_error_turn2 = True
        self.home_is_full = None

        printc(f"Čísla na kostkách: {self.dice1_value}, {self.dice2_value}", "green")

        while self.dice_values_list:

            if len(self.dice_values_list) == 0:
                break

            if backgammon.bearing_off_black == 15:
                break

            self.legal_moves_black_ai()
            self.ai_tag()

            if len(self.dice_values_list) == 0:
                break

            if backgammon.bearing_off_black == 15:
                break

            is_error_turn3 = True

            if self.bar_black_value == 0:

                while is_error_turn1:
                    is_error_turn2 = True

                    printc("AI: číslo poli = " + str(self.number_point_from) +
                           ", kost = " + str(self.user_turn_value), "blue")

                    if 1 <= self.number_point_from <= 24:

                        for key in self.board.keys():
                            if key == self.number_point_from:
                                if self.board[self.number_point_from] < 0:

                                    is_error_turn1 = False

                                else:
                                    print("AI: Na daném poli není žádného vašého kamenu.")
                                    print(self.dice_values_list)
                                    print(self.possible_turns_allow_pole)
                                    print(self.possible_turns_allow_kost)
                                    exit(1)

                    else:
                        print("AI: Zadejte číslo od 1 do 24.")
                        print(self.dice_values_list)
                        print(self.possible_turns_allow_pole)
                        print(self.possible_turns_allow_kost)
                        exit(1)

                while is_error_turn2:
                    is_error_turn1 = True

                    if self.user_turn_value in self.dice_values_list:
                        is_error_turn2 = False

                        try:
                            if self.board[self.number_point_from + self.user_turn_value] >= 2:
                                is_error_turn2 = True
                                print("AI: Nelze přesunout kamen, pole je obsazeno oponentem.")
                                print(self.dice_values_list)
                                print(self.possible_turns_allow_pole)
                                print(self.possible_turns_allow_kost)
                                exit(1)
                                break
                            elif self.board[self.number_point_from + self.user_turn_value] == 1:
                                self.board[self.number_point_from] += 1
                                self.board[self.number_point_from + self.user_turn_value] -= 2
                                self.dice_values_list.remove(self.user_turn_value)
                                self.bar_white_value += 1
                                printc("AI: Kamen oponenta byl vyhozen.", "yellow")
                                # запишем в историю этот ход черных
                                self.history_game.append(-self.number_point_from)  # Запоминаем выбраную позицию
                                self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                            else:
                                self.board[self.number_point_from] += 1
                                self.board[self.number_point_from + self.user_turn_value] -= 1
                                self.dice_values_list.remove(self.user_turn_value)
                                print("AI: Kamen byl přesunen.")
                                # запишем в историю этот ход черных
                                self.history_game.append(-self.number_point_from)  # Запоминаем выбраную позицию
                                self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень

                        except KeyError:
                            if self.home_is_full:
                                self.board[self.number_point_from] += 1
                                self.bearing_off_black += 1
                                self.dice_values_list.remove(self.user_turn_value)
                                printc("AI: Kamen byl vyveden.", "blue")
                                # запишем в историю этот ход черных
                                self.history_game.append(-self.number_point_from)  # Запоминаем выбраную позицию
                                self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                            else:
                                is_error_turn2 = True
                                print("AI: Nemůžete vyvest kamen pokud nemáte je všech doma.")
                                print(self.dice_values_list)
                                print(self.possible_turns_allow_pole)
                                print(self.possible_turns_allow_kost)

                                exit(1)
                                break

                    else:
                        print("AI: Zadejte číslo podle kostky (1).")
                        print(self.dice_values_list)
                        print(self.possible_turns_allow_pole)
                        print(self.possible_turns_allow_kost)
                        exit(1)

            else:
                if self.bar_black_value:

                    possible_turns = []
                    for value in self.dice_values_list:
                        for i in range(self.bar_black_value):

                            if self.board[value] >= 2:
                                possible_turns.append(0)
                            else:
                                possible_turns.append(1)

                    if 1 in possible_turns:

                        while is_error_turn3:

                            printc("\nAI: Musím vyvest kamen z baru, kost = " + str(self.user_turn_value), "green")

                            if self.user_turn_value in self.dice_values_list:

                                if self.board[self.user_turn_value] >= 2:
                                    printc("AI: Nelze přesunout kamen, pole je obsazeno oponentem.", "red")
                                    print(self.dice_values_list)
                                    print(self.possible_turns_allow_pole)
                                    print(self.possible_turns_allow_kost)
                                    exit(1)

                                elif self.board[self.user_turn_value] == 1:
                                    is_error_turn3 = False
                                    self.bar_black_value -= 1
                                    self.board[self.user_turn_value] -= 2
                                    self.dice_values_list.remove(self.user_turn_value)
                                    self.bar_white_value += 1
                                    printc("AI: Kamen oponenta byl vyhozen.", "yellow")
                                    # запишем в историю этот ход черных
                                    self.history_game.append(-self.user_turn_value)  # Запоминаем выбраную позицию
                                    self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень
                                else:
                                    is_error_turn3 = False
                                    self.bar_black_value -= 1
                                    self.board[self.user_turn_value] -= 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    print("AI: Kamen byl přesunen.")
                                    # запишем в историю этот ход черных
                                    self.history_game.append(-self.user_turn_value)  # Запоминаем выбраную позицию
                                    self.history_game.append(self.user_turn_value)  # Запоминаем выбраный камень

                            else:
                                print("AI: Zadejte číslo podle kostky (2).")
                                print(self.dice_values_list)
                                print(self.possible_turns_allow_pole)
                                print(self.possible_turns_allow_kost)
                                exit(1)

                    else:
                        printc("\nAI: Není možno uvést kamen na desku. Propuskaju tag !", "red")
                        print(self.dice_values_list)
                        print(self.possible_turns_allow_pole)
                        print(self.possible_turns_allow_kost)
                        self.dice_values_list = []
                        break


def save_history_json(datas):
    with open('history.dat', 'w') as outfile:
        json.dump(datas, outfile)


def save_ai_good_tags(datas):
    with open('ai_good.dat', 'w') as outfile:
        json.dump(datas, outfile)


def read_ai_good_tags(datas):
    with open('ai_good.dat') as json_file:
        data = json.load(json_file)
        for p in data:
            datas.append(p)


def save_ai_bad_tags(datas):
    with open('ai_bad.dat', 'w') as outfile:
        json.dump(datas, outfile)


def read_ai_bad_tags(datas):
    with open('ai_bad.dat') as json_file:
        data = json.load(json_file)
        for p in data:
            datas.append(p)


run = True
game = True
backgammon = Backgammon()


def cls():
    print("\n" * 100)


def printc(text, cl):
    if cl == "yellow":
        print("\033[33m{}\033[0m".format(text))
    elif cl == "blue":
        print("\033[34m{}\033[0m".format(text))
    elif cl == "red":
        print("\033[31m{}\033[0m".format(text))
    elif cl == "green":
        print("\033[32m{}\033[0m".format(text))
    elif cl == "violet":
        print("\033[35m{}\033[0m".format(text))
    elif cl == "turquoise":
        print("\033[36m{}\033[0m".format(text))
    else:
        print("\033[0m{}".format(text))


# основной игровой цикл

cls()
init()

while run:

    menu_test = True
    while menu_test:
        printc(
            "------------------------------------------------------------\n                          MENU                          "
            "\n------------------------------------------------------------", 'white')
        print("1. Hra dvou hráčů")
        print("2. Hra proti jednoduché umělé inteligenci")
        print("3. Pravidla hry")

        print("0. Ukončení hry")
        print("")

        menu = input("Váš výběr: ")
        if menu.isnumeric():
            menu = int(menu)
            if (menu < 0) or (menu > 3):
                print("")
                printc("Taková možnost neexistuje!", "red")
                printc("Vyberte znovu", "red")
                print("")
            else:
                if menu == 1:
                    ai = False
                    menu_test = False
                elif menu == 2:
                    ai = True
                    menu_test = False
                elif menu == 3:
                    # Выводим правила игрі
                    with open("pravidla.txt", "r", encoding="utf-8") as fl:
                        line_count = 34
                        for line in fl:
                            if line_count != 0:
                                printc(line.split("\n")[0], "yellow")
                                line_count -= 1
                            else:
                                line_count = 34
                                print("")
                                input('Stisknutím tlačítka "Enter" zobrazíte více...')
                                print("")
                    menu_test = True
                    print("")
                else:
                    print("")
                    printc("Konec hry! Na shledanou!", "blue")
                    exit(0)
        else:
            print("")
            printc("Taková možnost neexistuje! Vyberte číslo od 0 do 3.", "red")
            printc("Vyberte znovu", "red")
            print("")

    printc(
        "------------------------------------------------------------\n                     NOVA HRA!                      "
        "\n------------------------------------------------------------", "green")
    print("")

    read_ai_good_tags(backgammon.datas_ai_good)
    read_ai_bad_tags(backgammon.datas_ai_bad)

    who_is_first = backgammon.who_is_first()
    if who_is_first == "White":

        backgammon.history_game.append(99)  # Первая запись в историю ( 99 - первыми ходят белые)
        backgammon.roll_dices()
        backgammon.white_turn()
        save_history_json(backgammon.history_game)
        print("")
        while game:
            backgammon.roll_dices()

            if ai:
                backgammon.ai_turn()
            else:
                backgammon.black_turn()

            save_history_json(backgammon.history_game)
            print("")

            if backgammon.bearing_off_black == 15:
                backgammon.print_board()
                print("")
                print("Vyhráli černé.")
                print("")
                if backgammon.bearing_off_white > 0:
                    print('Úroveň výhry: "BĚŽNÁ VÝHRA"')

                else:
                    fishka_in_desk = False
                    for i in backgammon.board.values():
                        if i > 0:
                            fishka_in_desk = True

                    if (backgammon.bearing_off_white == 0) and (fishka_in_desk or (backgammon.bar_white_value > 0)):
                        print('Úroveň výhry: "BACKGAMMON"')

                    else:
                        print('Úroveň výhry: "GAMMON"')

                backgammon.history_game.append(0)
                save_ai_good_tags(backgammon.datas_ai_good + backgammon.history_game)
                game = False
                run = True

            else:
                backgammon.roll_dices()
                backgammon.white_turn()

            save_history_json(backgammon.history_game)
            print("")
            if backgammon.bearing_off_white == 15:
                backgammon.print_board()
                print("")
                print("Vyhráli bílé.")
                print("")
                if backgammon.bearing_off_white > 0:
                    print('Úroveň výhry: "BĚŽNÁ VÝHRA"')

                else:
                    fishka_in_desk = False
                    for i in backgammon.board.values():
                        if i < 0:
                            fishka_in_desk = True

                    if (backgammon.bearing_off_black == 0) and (fishka_in_desk or (backgammon.bar_black_value > 0)):
                        print('Úroveň výhry: "BACKGAMMON"')

                    else:
                        print('Úroveň výhry: "GAMMON"')

                backgammon.history_game.append(0)
                save_ai_bad_tags(backgammon.datas_ai_bad + backgammon.history_game)
                game = False
                run = True
    else:
        backgammon.history_game.append(-99)  # Первая запись в историю ( -99 - первыми ходят черные)
        save_history_json(backgammon.history_game)
        backgammon.roll_dices()

        if ai:
            backgammon.ai_turn()
        else:
            backgammon.black_turn()

        save_history_json(backgammon.history_game)
        print("")
        while game:
            backgammon.roll_dices()
            backgammon.white_turn()
            save_history_json(backgammon.history_game)
            print("")
            if backgammon.bearing_off_white == 15:
                backgammon.print_board()
                print("")
                print("Vyhráli bílé.")
                print("")
                if backgammon.bearing_off_white > 0:
                    print('Úroveň výhry: "BĚŽNÁ VÝHRA"')

                else:
                    fishka_in_desk = False
                    for i in backgammon.board.values():
                        if i < 0:
                            fishka_in_desk = True

                    if (backgammon.bearing_off_black == 0) and (fishka_in_desk or (backgammon.bar_black_value > 0)):
                        print('Úroveň výhry: "BACKGAMMON"')

                    else:
                        print('Úroveň výhry: "GAMMON"')
                backgammon.history_game.append(0)
                save_ai_bad_tags(backgammon.datas_ai_bad + backgammon.history_game)
                game = False
                run = True

            else:
                backgammon.roll_dices()

                if ai:
                    backgammon.ai_turn()
                else:
                    backgammon.black_turn()

            save_history_json(backgammon.history_game)
            print("")
            if backgammon.bearing_off_black == 15:
                backgammon.print_board()
                print("")
                print("Vyhráli černé.")
                print("")
                if backgammon.bearing_off_white > 0:
                    print('Úroveň výhry: "BĚŽNÁ VÝHRA"')

                else:
                    fishka_in_desk = False
                    for i in backgammon.board.values():
                        if i > 0:
                            fishka_in_desk = True

                    if (backgammon.bearing_off_white == 0) and (fishka_in_desk or (backgammon.bar_white_value > 0)):
                        print('Úroveň výhry: "BACKGAMMON"')

                    else:
                        print('Úroveň výhry: "GAMMON"')
                backgammon.history_game.append(0)
                save_ai_good_tags(backgammon.datas_ai_good + backgammon.history_game)
                game = False
                run = True
