from service import Service


class UI:
    def __init__(self):
        self.__size = self.get_input("file.txt")[0]
        self.__apples = self.get_input("file.txt")[1]
        self.__service = Service(self.__size, self.__apples)

    def get_input(self, file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()
            n = int(lines[0])
            apples = int(lines[1])
            f.close()
        return n, apples

    def make_move(self, command):
        if len(command) == 1:
            command[0] = command[0].lower()
            if command[0] != "up" and command[0] != "down" and command[0] != "left" and command[0] != "right" and command[0] != "move":
                raise ValueError("Invalid input")
            self.__service.set_direction(command[0])
            if self.__service.move_snake_one_square() == -1:
                return False

        elif len(command) == 2:
            command[0] = command[0].lower()
            if command[0] != "move":
                raise ValueError("Invalid input")
            if command[1].isdigit() is False:
                raise ValueError("Invalid input")
            for _ in range(int(command[1])):
                if self.__service.move_snake_one_square() == -1:
                    return False

        else:
            raise ValueError("Invalid input")


    def run(self):
        self.__service.place_snake()
        self.__service.place_apples()
        print(self.__service.get_board())

        while True:
            try:
                command = input(">>> ")
                list_of_commands = command.split()

                if self.make_move(list_of_commands) is False:
                    print("Game over!")
                    break

                print(self.__service.get_board())
            except Exception as e:
                print(e)

