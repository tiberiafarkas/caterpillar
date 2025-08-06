import os
import time

import pygame
import sys

from board import Board
from service import Service

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 80  # Each cell is 75x75 pixels

# Colors
BACKGROUND_COLOR = (30, 30, 30)
CATERPILLAR_COLOR = (0, 255, 0)
HEAD_COLOR = (255, 215, 0)
BUTTERFLY_COLOR = (255, 0, 255)
EYE_COLOR = (0, 0, 0)

# Load face image
face_image = pygame.image.load("vancea.jpg")
face_image = pygame.transform.scale(face_image, (CELL_SIZE, CELL_SIZE))


class GameGUI:
    def __init__(self):
        self.size = 0
        self.apples = 0
        self.service = Service(0, 0)
        self.board = Board(0, 0)
        self.GRID_SIZE = self.board.get_size()
        self.SCREEN_SIZE = CELL_SIZE * self.GRID_SIZE
        self.FPS = 8        #frames per second
        self.service.place_snake()
        self.service.place_apples()
        self.MENU_SCREEN_SIZE = 560  # Fixed screen size for the menu
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))
        pygame.display.set_caption("Caterpillar Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.started = False  # Caterpillar does not move initially


    def draw_grid(self, screen):
        for x in range(0, self.SCREEN_SIZE, CELL_SIZE):
            for y in range(0, self.SCREEN_SIZE, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid(self.screen)
        board = self.service.get_board()


        for (x, y) in board.get_snake():
            pygame.draw.circle(self.screen, CATERPILLAR_COLOR,
                               (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2),
                               CELL_SIZE // 3)
        head_x, head_y = board.get_snake()[0]
        pygame.draw.circle(self.screen, HEAD_COLOR,
                           (head_y * CELL_SIZE + CELL_SIZE // 2,
                            head_x * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 3)

        # Draw eyes
        eye_offset = CELL_SIZE // 8
        eye_radius = CELL_SIZE // 10
        pygame.draw.circle(self.screen, EYE_COLOR,
                           (head_y * CELL_SIZE + CELL_SIZE // 3,
                            head_x * CELL_SIZE + CELL_SIZE // 3), eye_radius)
        pygame.draw.circle(self.screen, EYE_COLOR,
                           (head_y * CELL_SIZE + 2 * CELL_SIZE // 3,
                            head_x * CELL_SIZE + CELL_SIZE // 3), eye_radius)

        for (x, y) in board.get_apples():
            self.screen.blit(face_image, (y * CELL_SIZE, x * CELL_SIZE))

        pygame.display.flip()

    def butterfly_animation(self):
        for i in range(5):
            self.screen.fill(BACKGROUND_COLOR)
            pygame.draw.circle(self.screen, BUTTERFLY_COLOR, (self.SCREEN_SIZE // 2, self.SCREEN_SIZE // 2), (i + 1) * 20)
            pygame.display.flip()
            pygame.time.delay(300)

    def choose_difficulty(self):
        """
        player chooses the difficulty level
        :return:
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.MENU_SCREEN_SIZE // 2 - 100 <= x <= self.MENU_SCREEN_SIZE // 2 + 100:
                        if self.MENU_SCREEN_SIZE // 2 + 50 <= y <= self.MENU_SCREEN_SIZE // 2 + 100:
                            difficulty = "easy"
                            self.FPS = 3
                            self.size = 5
                            self.apples = 3
                        elif self.MENU_SCREEN_SIZE // 2 + 100 <= y <= self.MENU_SCREEN_SIZE // 2 + 150:
                            difficulty = "medium"
                            self.FPS = 5
                            self.size = 7
                            self.apples = 8
                        elif self.MENU_SCREEN_SIZE // 2 + 150 <= y <= self.MENU_SCREEN_SIZE // 2 + 200:
                            difficulty = "hard"
                            self.size = 10
                            self.apples = 10
                            self.FPS = 8
                        else:
                            continue

                        # Reset the game state after choosing difficulty
                        self.service = Service(self.size, self.apples)
                        self.service.set_difficulty(difficulty)
                        # self.service.place_snake()
                        # self.service.place_apples()
                        self.running = True

                        # Get new board size
                        self.board = self.service.get_board()
                        self.GRID_SIZE = self.board.get_size()
                        self.SCREEN_SIZE = CELL_SIZE * self.GRID_SIZE  # Fix screen size update
                        self.screen = pygame.display.set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))

                        return

    def display_menu(self):
        """
        display the buttons for choosing the difficulty level
        easy - a 5x5 grid with 3 apples and fps = 3
        medium - a 7x7 grid with 8 apples and fps = 5
        hard - a 10x10 grid with 10 apples and fps = 8
        """
        self.screen = pygame.display.set_mode((self.MENU_SCREEN_SIZE, self.MENU_SCREEN_SIZE))
        self.screen.fill(BACKGROUND_COLOR)

        text = pygame.font.SysFont("Arial", 50).render("Caterpillar Game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.MENU_SCREEN_SIZE // 2, self.MENU_SCREEN_SIZE // 2 - 50))
        self.screen.blit(text, text_rect)

        easy_button = pygame.Rect(self.MENU_SCREEN_SIZE // 2 - 100, self.MENU_SCREEN_SIZE // 2 + 50, 200, 50)
        pygame.draw.rect(self.screen, (0, 255, 0), easy_button)
        text = pygame.font.SysFont("Arial", 30).render("Easy", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.MENU_SCREEN_SIZE // 2, self.MENU_SCREEN_SIZE // 2 + 75))
        self.screen.blit(text, text_rect)

        medium_button = pygame.Rect(self.MENU_SCREEN_SIZE // 2 - 100, self.MENU_SCREEN_SIZE // 2 + 100, 200, 50)
        pygame.draw.rect(self.screen, (255, 255, 0), medium_button)
        text = pygame.font.SysFont("Arial", 30).render("Medium", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.MENU_SCREEN_SIZE // 2, self.MENU_SCREEN_SIZE // 2 + 125))
        self.screen.blit(text, text_rect)

        hard_button = pygame.Rect(self.MENU_SCREEN_SIZE // 2 - 100, self.MENU_SCREEN_SIZE // 2 + 150, 200, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), hard_button)
        text = pygame.font.SysFont("Arial", 30).render("Hard", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.MENU_SCREEN_SIZE // 2, self.MENU_SCREEN_SIZE // 2 + 175))
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.choose_difficulty()

    def restart_game(self):
        """
        player press the restart button or quit button and the game is restarted or quit
        :return:
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.SCREEN_SIZE // 2 - 100 <= x <= self.SCREEN_SIZE // 2 + 100:
                        if self.SCREEN_SIZE // 2 + 50 <= y <= self.SCREEN_SIZE // 2 + 100:
                            self.display_menu()
                            self.service = Service(self.size, self.apples)
                            self.service.place_snake()
                            self.service.place_apples()
                            self.running = True
                            self.started = False
                            return
                        elif self.SCREEN_SIZE // 2 + 125 <= y <= self.SCREEN_SIZE // 2 + 200:
                            self.running = False
                            return


    def draw_restart_game(self):
        """
        The game is over, the buttons for restarting the game or quitting are displayed
        :return:
        """
        self.screen.fill(BACKGROUND_COLOR)
        text = pygame.font.SysFont("Arial", 50).render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.SCREEN_SIZE // 2, self.SCREEN_SIZE // 2 - 50))
        self.screen.blit(text, text_rect)

        restart_button = pygame.Rect(self.SCREEN_SIZE // 2 - 100, self.SCREEN_SIZE // 2 + 50, 200, 50)
        pygame.draw.rect(self.screen, (0, 255, 0), restart_button)
        text = pygame.font.SysFont("Arial", 30).render("Restart", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.SCREEN_SIZE // 2, self.SCREEN_SIZE // 2 + 75))
        self.screen.blit(text, text_rect)

        quit_button = pygame.Rect(self.SCREEN_SIZE // 2 - 100, self.SCREEN_SIZE // 2 + 125, 200, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), quit_button)
        text = pygame.font.SysFont("Arial", 30).render("Quit", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.SCREEN_SIZE // 2, self.SCREEN_SIZE // 2 + 150))
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.restart_game()

    def game_over(self):
        print("Game Over")
        self.running = False
        time.sleep(1)
        self.draw_restart_game()

    def run(self):
        self.display_menu()
        while self.running:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        try:
                            self.service.set_direction("up")
                            self.started = True
                        except ValueError:
                            self.game_over()

                    elif event.key == pygame.K_DOWN:
                        try:
                            self.service.set_direction("down")
                            self.started = True
                        except ValueError:
                            self.game_over()
                    elif event.key == pygame.K_LEFT:
                        try:
                            self.service.set_direction("left")
                            self.started = True
                        except ValueError:
                            self.game_over()
                    elif event.key == pygame.K_RIGHT:
                        try:
                            self.service.set_direction("right")
                            self.started = True
                        except ValueError:
                            self.game_over()

            if self.started:
                if self.service.move_snake_one_square() == -1:
                    self.game_over()

            if len(self.board.get_snake()) == self.GRID_SIZE * self.GRID_SIZE:
                self.butterfly_animation()
                print("You win! Caterpillar transforms into a butterfly!")
                self.running = False

            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    GameGUI().run()
