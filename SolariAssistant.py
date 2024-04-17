#   Author:
#                   Matt Tucker
#
#   Date:
#                   14Apr2024
#
#   Description:
#                   The following is a "chat assistant" that delivers response via a Solari(Split-flap) Board
#
#   Notes:
#                   May be fun to build agents into this... Could make it more versatile, robust, and all around more
#                   useful. It could also have tha added benefit of making it seem "more human."
#
#   ToDo:
#                   Build out "chat" and "data retrieval" classes; and, to address the second "if-statement" so that
#                   instead of "if event.type == pygame.KEYDOWN" we use a "wake-up" command(or something to that effect)
#                   and begin the process of interacting with the user.

import pygame
import sys
import speech_recognition as sr

# Initialize Pygame
pygame.init()

# Get the screen's current width and height for full-screen mode
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Constants
SPRITE_SIZE = 26
COLUMNS = 25
ROWS = 34
COLUMN_DELAY = 850  # Delay between columns in milliseconds

class SolariBoard:
    def __init__(self, screen, sprite_sheet_path):
        self.screen = screen
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.total_sprites = 256  # Total sprites available
        self.sprites = [self.get_sprite(i) for i in range(0, self.total_sprites, 2)]  # Load sprites from even indices
        self.ascii_to_sprite_index = {i: [2 * (i - 32), 2 * ((i - 32) + 32)] for i in range(32, 96)}
        self.display_grid = [[' '] * COLUMNS for _ in range(ROWS)]
        self.current_indices = [[0] * COLUMNS for _ in range(ROWS)]
        # Calculate the starting X to center the board horizontally
        self.start_x = (WIDTH - COLUMNS * (SPRITE_SIZE + 2)) // 2
        self.start_y = (HEIGHT - ROWS * (SPRITE_SIZE + 2)) // 2

    def get_sprite(self, index):
        x = (index % (self.sprite_sheet.get_width() // SPRITE_SIZE)) * SPRITE_SIZE
        y = (index // (self.sprite_sheet.get_width() // SPRITE_SIZE)) * SPRITE_SIZE
        return self.sprite_sheet.subsurface((x, y, SPRITE_SIZE, SPRITE_SIZE))

    def place_sprites(self):
        self.screen.fill((0, 0, 0))
        for row in range(ROWS):
            for col in range(COLUMNS):
                sprite_index = self.current_indices[row][col] // 2
                if sprite_index < len(self.sprites):
                    sprite = self.sprites[sprite_index]
                    x = col * (SPRITE_SIZE + 2) + self.start_x
                    y = row * (SPRITE_SIZE + 2) + self.start_y
                    self.screen.blit(sprite, (x, y))
        pygame.display.flip()

    def set_sprite_values(self, message):
        words = message.split()
        row, col = 0, 0
        for word in words:
            if col + len(word) > COLUMNS:
                row += 1
                col = 0
            if row >= ROWS:
                break
            for char in word:
                if col < COLUMNS:
                    self.display_grid[row][col] = char
                    col += 1
            if col < COLUMNS:
                self.display_grid[row][col] = ' '
                col += 1
            if col >= COLUMNS:
                row += 1
                col = 0
        self.place_sprites()

    def animate_to_message(self, message):
        self.set_sprite_values(message)
        start_times = [pygame.time.get_ticks() + i * COLUMN_DELAY for i in range(COLUMNS)]
        completed = [False] * COLUMNS

        while not all(completed):
            current_time = pygame.time.get_ticks()
            for col in range(COLUMNS):
                if not completed[col] and current_time >= start_times[col]:
                    completed[col] = True
                    for row in range(ROWS):
                        target_char = self.display_grid[row][col]
                        if target_char != ' ' and ord(target_char) in self.ascii_to_sprite_index:
                            target_indices = self.ascii_to_sprite_index[ord(target_char)]
                            target_index = target_indices[0]
                            if self.current_indices[row][col] != target_index:
                                self.current_indices[row][col] = (self.current_indices[row][col] + 1) % self.total_sprites
                                completed[col] = False
                    self.place_sprites()
                    pygame.time.delay(5)  # Adjust flipping speed

class ChatBot:
    def __init__(self):
        self.command = ''

    # Needs modification, this is old and from https://tuckersideas.net/2017/08/16/chatbot-digital-assistant/
    def listener(self):
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # r.adjust_for_ambient_noise(source)
            print("I'm listening")
            audio = r.listen(source)
        # Speech recognition
        data = ""
        try:
            data = r.recognize_google(audio)
            if data == "end program":
                exit()
            print("You said: " + data)
        except sr.UnknownValueError:
            board.animate_to_message("Can you please repeat that")
            self.listener()
        except sr.RequestError as e:
            board.animate_to_message("Can you please repeat that?".format(e))
            self.listener()
        self.command = data
    # def paser():
    # def dataGetter():
    # def response():

class InformationRetrieval:
    def __init__(self, user_req):
        self.command = user_req
    # def wikiHandler():
    # def stackOverflow():
    # def weather():
    # def mathematica():
    # def arxiv():


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Set to fullscreen
    pygame.display.set_caption("Solari Board Simulation")
    bot = ChatBot()
    global board
    board = SolariBoard(screen, './letters-final.png')
    board.set_sprite_values("HELLO WORLD THIS IS A TEST MESSAGE THAT SHOULD WRAP CORRECTLY")  # Set initial message
    running = True
    while running:
        bot.listener()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_message = "ANOTHER LONG MESSAGE THAT WILL NEED TO WRAP ACROSS MULTIPLE LINES TO FIT PROPERLY"
                    board.animate_to_message(new_message)  # Animate to the new message
                if event.key == pygame.K_ESCAPE:  # Allow closing the fullscreen with ESC
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
