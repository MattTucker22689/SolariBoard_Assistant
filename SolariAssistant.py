#   Author:
#                   Matt Tucker
#
#   Date:
#                   14Apr2024 - 25Apr2024
#
#   Description:
#                   The following is a 'chat assistant' that delivers response via a Solari(Split-flap) Board
#
#   Notes:
#                   May be fun to build agents into this... Could make it more versatile, robust, and all-around more
#                   useful. It could also have the added benefit of making it seem 'more human.'
#
#   ToDo:
#                   Build out 'chat' and 'data retrieval' classes; and, to address the second 'if-statement' so that
#                   instead of 'if event.type == pygame.KEYDOWN' we use a 'wake-up' command(or something to that effect)
#                   and begin the process of interacting with the user.

import pygame
import sys
import speech_recognition as sr

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1415, 967
SPRITE_SIZE = 26
COLUMNS = 50
ROWS = 34
COLUMN_DELAY = 850  # Delay between columns in milliseconds

class SolariBoard:
    def __init__(self, screen, sprite_sheet_path):
        self.screen = screen
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.total_sprites = 256  # Total sprites available
        self.sprites = [self.get_sprite(i) for i in range(0, self.total_sprites, 2)]  # Load sprites from even indices
        self.ascii_to_sprite_index = {i: [2 * (i - 32), 2 * ((i - 32) + 32)] for i in range(32, 96)}  # Two mappings for each ASCII value
        self.display_grid = [[' '] * COLUMNS for _ in range(ROWS)]
        self.current_indices = [[0] * COLUMNS for _ in range(ROWS)]  # Current sprite indices

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
                    x = col * (SPRITE_SIZE + 2) + 10
                    y = row * (SPRITE_SIZE + 2) + 10
                    self.screen.blit(sprite, (x, y))
        pygame.display.flip()

    def set_sprite_values(self, message):
        flat_list = list(message) + [' '] * (ROWS * COLUMNS - len(message))
        self.display_grid = [flat_list[i * COLUMNS:(i + 1) * COLUMNS] for i in range(ROWS)]
        self.place_sprites()

    def animate_to_message(self, message):
        self.set_sprite_values(message)
        # Start times for each column based on current time + delay
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
                            target_index = target_indices[0]  # Simplify by choosing the first index
                            # Perform one step in animation for each row in this column
                            if self.current_indices[row][col] != target_index:
                                self.current_indices[row][col] = (self.current_indices[row][col] + 1) % self.total_sprites
                                completed[col] = False
                    self.place_sprites()
                    pygame.time.delay(5)  # Faster flipping through characters

class ChatBot:
    def __init__(self):
        self.command = ''
    def listener(self):
        print('listening')
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        # Speech recognition
        data = ''
        try:
            data = r.recognize_google(audio)
            if data == 'end program':
                exit()
            print('You said: ' + data)
            if 'I need help' in data:
                print('Temp')
        except sr.UnknownValueError:
            print('Can you please repeat that')
            self.listener()
        except sr.RequestError as e:
            print('Can you please repeat that? '.format(e))
            self.listener()
        board.animate_to_message(data.upper())

    def inputClassifier(self):
        # Classify if request is for weather, and inquiry, directed at pi as conversation, or ignorable
        # Temp pattern
        pass

    def dataGetter(self):
        # Review and summarize data from information retrieval
        # Temp pattern
        pass

    def response(self):
        # Crafts response
        # Temp pattern
        pass

class InformationRetrieval:
    def __init__(self, user_req):
        self.command = user_req

    def weather(self):
        # Get weather data
        # Temp pattern
        pass

    def wolfram(self):
        # Retrieves information from Wolfram Alpha
        # Temp pattern
        pass

    def wikiHandler(self):
        # Retrieves information from Wikipedia
        # Temp pattern
        pass

    ### -Hold on to these for later-
    # def stackOverflow():
    # def arxiv():


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Solari Board Simulation')
    global board
    board = SolariBoard(screen, './letters-final.png')
    board.set_sprite_values(' ')  # Set initial message
    chat = ChatBot()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_message = 'Short Test'
                    board.animate_to_message(new_message.upper())  # Animate to the new message
                    chat.listener()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
