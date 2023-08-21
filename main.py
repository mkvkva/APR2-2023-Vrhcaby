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

    # основная игровая функция, реализующая ход белых шашек
    def white_turn(self):
        print("----------\nTAH BÍLÝCH\n----------")

        is_error_turn1 = True
        is_error_turn2 = True
        home_is_full = None

        print(f"Čísla na kostkách: {self.dice1_value}, {self.dice2_value}")

        while self.dice_values_list:

            is_error_turn3 = True

            if self.bar_white_value == 0:

                # иногда на протежении игры могут происходить ситуации когда невозможно походить ни одной из шашек,
                # этот блок кода проверяет возможно ли сделать хотя бы одно перемещение шашки за ход
                # если невозможно - игрок пропускает ход
                for key in self.board.keys():
                    if 7 <= key <= 24:
                        if self.board[key] > 0:
                            home_is_full = False
                            break
                        else:
                            home_is_full = True

                possible_turns = []
                for value in self.dice_values_list:
                    for key in self.board.keys():
                        if self.board[key] > 0:

                            try:
                                if self.board[key-value] <= -2:
                                    possible_turns.append(0)
                                else:
                                    possible_turns.append(1)
                            except KeyError:
                                if home_is_full:
                                    possible_turns.append(1)
                                else:
                                    possible_turns.append(0)

                if 1 in possible_turns:
                    pass
                else:
                    print("\nNení možno udělat žádný tah.")
                    self.dice_values_list = []
                    break

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
                                        print("Na daném poli není žádného vašého kamenu.")

                        else:
                            print("Zadejte číslo od 1 do 24.")
                    else:
                        print("Zadejte číslo od 1 do 24.")

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
                                if self.board[self.number_point_from-self.user_turn_value] <= -2:
                                    is_error_turn2 = True
                                    print("Nelze přesunout kamen, pole je obsazeno oponentem.")
                                    break
                                elif self.board[self.number_point_from-self.user_turn_value] == -1:
                                    self.board[self.number_point_from] -= 1
                                    self.board[self.number_point_from-self.user_turn_value] += 2
                                    self.dice_values_list.remove(self.user_turn_value)
                                    self.bar_black_value += 1
                                    print("Kamen oponenta byl vyhozen.")
                                else:
                                    self.board[self.number_point_from] -= 1
                                    self.board[self.number_point_from-self.user_turn_value] += 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    print("Kamen byl přesunen.")

                            except KeyError:

                                if home_is_full:
                                    self.board[self.number_point_from] -= 1
                                    self.bearing_off_white += 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    print("Kamen byl vyveden.")
                                else:
                                    is_error_turn2 = True
                                    print("Nemůžete vyvest kamen pokud nemáte je všech doma.")
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

                            print("\nMusíte vyvest kamen z baru.", end=" ")
                            self.user_turn_value = input("Zadejte hodnotu svého tahu podle kostky: ")
                            if self.user_turn_value.isnumeric():
                                self.user_turn_value = int(self.user_turn_value)
                                if self.user_turn_value in self.dice_values_list:

                                    if self.board[25-self.user_turn_value] <= -2:
                                        print("Nelze přesunout kamen, pole je obsazeno oponentem.")
                                    elif self.board[25-self.user_turn_value] == -1:
                                        is_error_turn3 = False
                                        self.bar_white_value -= 1
                                        self.board[25-self.user_turn_value] += 2
                                        self.dice_values_list.remove(self.user_turn_value)
                                        self.bar_black_value += 1
                                        print("Kamen oponenta byl vyhozen.")
                                    else:
                                        is_error_turn3 = False
                                        self.bar_white_value -= 1
                                        self.board[25-self.user_turn_value] += 1
                                        self.dice_values_list.remove(self.user_turn_value)
                                        print("Kamen byl přesunen.")

                                else:
                                    print("Zadejte číslo podle kostky.")
                            else:
                                print("Zadejte číslo podle kostky.")

                    else:
                        print("\nNení možno uvést kamen na desku.")
                        self.dice_values_list = []
                        break

    # аналогичная функция для реализации хода, но уже для черных шашек
    def black_turn(self):
        print("----------\nTAH ČERNÝCH\n----------")

        is_error_turn1 = True
        is_error_turn2 = True
        home_is_full = None

        print(f"Čísla na kostkách: {self.dice1_value}, {self.dice2_value}")

        while self.dice_values_list:

            is_error_turn3 = True

            if self.bar_black_value == 0:

                for key in self.board.keys():
                    if 1 <= key <= 18:
                        if self.board[key] < 0:
                            home_is_full = False
                            break
                        else:
                            home_is_full = True

                possible_turns = []
                for value in self.dice_values_list:
                    for key in self.board.keys():
                        if self.board[key] < 0:

                            try:
                                if self.board[key+value] >= 2:
                                    possible_turns.append(0)
                                else:
                                    possible_turns.append(1)
                            except KeyError:
                                if home_is_full:
                                    possible_turns.append(1)
                                else:
                                    possible_turns.append(0)

                if 1 in possible_turns:
                    pass
                else:
                    print("\nNení možno udělat žádný tah.")
                    self.dice_values_list = []
                    break

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
                                if self.board[self.number_point_from+self.user_turn_value] >= 2:
                                    is_error_turn2 = True
                                    print("Nelze přesunout kamen, pole je obsazeno oponentem.")
                                    break
                                elif self.board[self.number_point_from+self.user_turn_value] == 1:
                                    self.board[self.number_point_from] += 1
                                    self.board[self.number_point_from+self.user_turn_value] -= 2
                                    self.dice_values_list.remove(self.user_turn_value)
                                    self.bar_white_value += 1
                                    print("Kamen oponenta byl vyhozen.")
                                else:
                                    self.board[self.number_point_from] += 1
                                    self.board[self.number_point_from+self.user_turn_value] -= 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    print("Kamen byl přesunen.")

                            except KeyError:

                                if home_is_full:
                                    self.board[self.number_point_from] += 1
                                    self.bearing_off_black += 1
                                    self.dice_values_list.remove(self.user_turn_value)
                                    print("Kamen byl vyveden.")
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
                                    else:
                                        is_error_turn3 = False
                                        self.bar_black_value -= 1
                                        self.board[self.user_turn_value] -= 1
                                        self.dice_values_list.remove(self.user_turn_value)
                                        print("Kamen byl přesunen.")

                                else:
                                    print("Zadejte číslo podle kostky.")
                            else:
                                print("Zadejte číslo podle kostky.")

                    else:
                        print("\nNení možno uvést kamen na desku.")
                        self.dice_values_list = []
                        break
