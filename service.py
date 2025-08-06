from random import randint

from board import Board


class Service:
    def __init__(self, size, apples):
        up = 0
        self.board = Board(size, apples)
        self.__last_direction = up

    def set_direction(self, direction):
        """
        check if the direction is valid
        and set the last direction
        up = 0
        down = 1
        left = 2
        right = 3

        :param direction:
        :return:
        """
        up = 0
        down = 1
        left = 2
        right = 3

        if direction == "up" and self.__last_direction == down:
            raise ValueError("Invalid direction")

        if direction == "down" and self.__last_direction == up:
            raise ValueError("Invalid direction")

        if direction == "left" and self.__last_direction == right:
            raise ValueError("Invalid direction")

        if direction == "right" and self.__last_direction == left:
            raise ValueError("Invalid direction")

        if direction == "up":
            self.__last_direction = up
        elif direction == "down":
            self.__last_direction = down
        elif direction == "left":
            self.__last_direction = left
        elif direction == "right":
            self.__last_direction = right

    def get_board(self):
        self.board.generate_board()
        return self.board

    def place_snake(self):
        self.board.place_snake()
        return self.board

    def place_apples(self):
        self.board.place_apples()
        return self.board

    def set_difficulty(self, difficulty):
        """
        Set the difficulty of the game
        :param difficulty:
        :return:
        """
        self.board.set_difficulty(difficulty)

    def move_snake_one_square(self):
        """
        Move the snake in the given direction
        Only the head and the tail are actually moved
        We will add a new head in the given direction and we will remove the tail
        We will also check if the snake has eaten an apple
        If it did, we will not remove the tail
        :param direction:
        :return:
        """
        self.board.set_direction(self.__last_direction)

        if self.board.direction == 0:
            i = -1
            j = 0
        elif self.board.direction == 1:
            i = 1
            j = 0
        elif self.board.direction == 2:
            i = 0
            j = -1
        else:
            i = 0
            j = 1

        head_x = self.board._snake[0][0]
        head_y = self.board._snake[0][1]

        if self.check_game_end(head_x + i, head_y + j):
            return -1

        self.board._snake.insert(0, (head_x + i, head_y + j))

        if (head_x + i, head_y + j) not in self.board._apples_list:
            self.board._snake.pop() #we remove the tail

        else:
            self.board._apples_list.remove((head_x + i, head_y + j))
            self.generate_apple()

        self.board.generate_board()

    def move_snake_more_squares(self, squares):
        """
        Move the snake multiple squares in one direction
        :param direction:
        :return:
        """
        for i in range(squares):
            if self.move_snake_one_square() is True:    #check_game_end = True
                return False

        return True

    def check_game_end(self, x, y):
        """
        Check if the game has ended
        :param x:
        :param y:
        :return:
        """
        if x < 0 or x >= self.board._size or y < 0 or y >= self.board._size:
            return True

        if (x, y) in self.board._snake:
            return True

        return False

    def check_empty_cells(self):
        """
        Check if there are empty cells
        :param x:
        :param y:
        :return:
        """
        for i in range(self.board._size):
            for j in range(self.board._size):
                if (i, j) not in self.board._snake or (i, j) not in self.board._apples_list or \
                    (i + 1, j) not in self.board._apples_list or (i - 1, j) not in self.board._apples_list or \
                    (i, j + 1) not in self.board._apples_list or (i, j - 1) not in self.board._apples_list:
                    return True

        return False


    def generate_apple(self):
        """
        Generate a new apple
        :return:
        """
        x = randint(0, self.board._size - 1)
        y = randint(0, self.board._size - 1)
        while (((x, y) in self.board._snake or (x, y) in self.board._apples_list or
               (x + 1, y) in self.board._apples_list or (x - 1, y) in self.board._apples_list or
               (x, y + 1) in self.board._apples_list or (x, y - 1) in self.board._apples_list) and
               self.check_empty_cells() is True):
            x = randint(0, self.board._size - 1)
            y = randint(0, self.board._size - 1)

        self.board._apples_list.append((x, y))
        self.board.generate_board()
