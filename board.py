from random import randint

import texttable as Texttable

"""
The game area is an NxN matrix of squares that contains the snake and several apples
The snake always start with a head segment (represented using "*") and 2 body segments (represented using "+")
and is placed in the middle of the board.
Apples are resented using an (a).
Apples are placed randomly, so that two apples cannot be adjacent to each other and cannot overlap the snake's starting position
The value N and the number of apples are read from a settings file.
"""

class Board:
    def __init__(self, size, apples):
        self._size = size
        self._snake = []
        self._apples = apples
        self._apples_list = []
        self._game_board = [[' ' for _ in range(self._size)] for _ in range(self._size)]
        self._direction = 0     #initial direction is up

    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            self._size = 5
            self._apples = 3
        elif difficulty == "medium":
            self._size = 7
            self._apples = 8
        else:
            self._size = 10
            self._apples = 10

        self._game_board = [[' ' for _ in range(self._size)] for _ in range(self._size)]
        self._snake = []
        self._apples_list = []

        self.place_snake()
        self.place_apples()
        self.generate_board()


    def get_input(self, file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()
            n = int(lines[0])
            apples = int(lines[1])
            f.close()
        return n, apples

    def generate_board(self):
        """
        Generate the board
        a -> apple
        * -> snake head
        + -> snake body
        :return:
        """

        for i in range(self._size):
            for j in range(self._size):
                if (i, j) in self._apples_list:
                    self._game_board[i][j] = 'a'
                elif (i, j) in self._snake:
                    if (i, j) == self._snake[0]:
                        self._game_board[i][j] = 'H'
                    else:
                        self._game_board[i][j] = '+'
                else:
                    self._game_board[i][j] = ' '

    def __str__(self):
        t = Texttable.Texttable()

        for i in range(self._size):
            row = []
            for j in range(self._size):
                row.append(self._game_board[i][j])
            t.add_row(row)

        return t.draw()

    def place_snake(self):
        """
        Place the snake on the board
        :return:
        """
        mid = self._size // 2
        if self._size % 2 == 0:  # If size is even, shift left by 1
            self._snake = [(mid - 2, mid - 1), (mid - 1, mid - 1), (mid, mid - 1)]
        else:
            self._snake = [(mid - 1, mid), (mid, mid), (mid + 1, mid)]
        self.generate_board()

    def place_apples(self):
        """
        Place the apples on the board
        :return:
        """
        for _ in range(self._apples):
            x = randint(0, self._size - 1)
            y = randint(0, self._size - 1)
            while ((x, y) in self._snake or (x, y) in self._apples_list or
                   (x + 1, y) in self._apples_list or (x - 1, y) in self._apples_list or
                   (x, y + 1) in self._apples_list or (x, y - 1) in self._apples_list):
                x = randint(0, self._size - 1)
                y = randint(0, self._size - 1)
            self._apples_list.append((x, y))
        self.generate_board()

    def get_snake(self):
        return self._snake

    def get_apples(self):
        return self._apples_list

    def get_size(self):
        return self._size



