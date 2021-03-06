import pygame, Board, time, sys, Oponent, random


class Button:
    def __init__(self, color, x, y, width, height, text, func):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.func = func

    def display(self):  # displays the button with text in the middle
        pygame.draw.rect(Board.game_display, self.color, (self.x, self.y, self.width, self.height))
        tw, th = Board.big_font.size(self.text)
        Board.display_text(self.text, Board.big_font, self.x + self.width/2 - tw/2, self.y + self.height/2 - th/2, (255, 255, 255))


def end_menu():
    global display_menu
    display_menu = False


def make_quit():
    pygame.quit()
    quit()
    return True


def to_white():  # swaps player color to white
    Board.player_color = "white"
    Board.computer_color = "black"
    Oponent.computer.color = "black"


def to_black():  # swaps player color to black
    Board.player_color = "black"
    Board.computer_color = "white"
    Oponent.computer.color = "white"


def to_random():  # randomly chooses player color
    Board.player_color = random.choice(["white", "black"])
    if Board.player_color == "white":
        Board.computer_color = "black"
        Oponent.computer.color = "black"
    else:
        Board.computer_color = "white"
        Oponent.computer.color = "white"


# difficulties
def easy():
    Board.ai_difficulty = 1


def medium():
    Board.ai_difficulty = 2


def hard():
    Board.ai_difficulty = 3


def menu():  # displays menu
    global display_menu
    display_menu = True
    # all the buttons in menu
    buttons = [Button((0, 0, 0), 320, 50, 200, 100, "Play", end_menu),
               Button((0, 0, 0), 70, 210, 200, 100, "White", to_white),
               Button((0, 0, 0), 570, 210, 200, 100, "Random", to_random),
               Button((0, 0, 0), 320, 210, 200, 100, "Black", to_black),
               Button((0, 0, 0), 70, 380, 200, 100, "Easy", easy),
               Button((0, 0, 0), 320, 380, 200, 100, "Medium", medium),
               Button((0, 0, 0), 570, 380, 200, 100, "Hard", hard),
               Button((0, 0, 0), 320, 530, 200, 100, "Help", help_screen),
               Button((0, 0, 0), 320, 680, 200, 100, "Quit", make_quit)]
    while display_menu:
        Board.game_display.fill((150, 150, 150))  # grey
        for button in buttons:
            button.display()
        Board.display_text("Choose your color", Board.big_font, 220, 150, (0, 0, 0))
        Board.display_text("Choose difficulty", Board.big_font, 233, 310, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():  # checks events
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    return True
                else:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in buttons:
                    if x in range(button.x, button.x + button.width + 1) and y in range(button.y, button.y + button.height + 1):
                        button.func()


def help_screen():
    Board.game_display.fill((100, 100, 100))
    # just display some advice on how to work with the app
    # damn this sucks
    # what am i supposed to tell them? To click the pieces and move them? Lmao
    Board.display_text("This is a help for the absolutely dumb ones.", Board.help_font, 80, 50, (0, 0, 0))
    Board.display_text("To quit this app press Q or click QUIT in menu.", Board.help_font, 50, 100, (0, 0, 0))
    Board.display_text("In the menu, press any key (except for Q) ", Board.help_font, 0, 150, (0, 0, 0))
    Board.display_text("to go to the game or just click PLAY.", Board.help_font, 60, 200, (0, 0, 0))
    Board.display_text("To quit this app press Q or click QUIT in menu.", Board.help_font, 60, 250, (0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                else:
                    return True
        pygame.display.update()


