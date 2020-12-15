import pygame, Board, time, sys, Oponent


def menu():
    while True:
        Board.game_display.fill((150, 150, 150)) # grey
        pygame.draw.rect(Board.game_display, (0, 0, 0), (320, 100, 200, 100))  # play
        pygame.draw.rect(Board.game_display, (0, 0, 0), (320, 600, 200, 100))  # quit
        pygame.draw.rect(Board.game_display, (0, 0, 0), (170, 300, 200, 100))  # white
        pygame.draw.rect(Board.game_display, (0, 0, 0), (470, 300, 200, 100))  # black
        pygame.draw.rect(Board.game_display, (0, 0, 0), (320, 450, 200, 100))  # help
        Board.display_text("Play", Board.big_font, 375, 120, (255, 255, 255))  # center the text properly
        Board.display_text("White", Board.big_font, 210, 320, (255, 255, 255))
        Board.display_text("Black", Board.big_font, 510, 320, (255, 255, 255))
        Board.display_text("Help", Board.big_font, 375, 470, (255, 255, 255))
        Board.display_text("Quit", Board.big_font, 375, 620, (255, 255, 255))
        Board.display_text("Choose your color", Board.big_font, 230, 210, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    return True
                else:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x in range(320, 521):
                    if y in range(100, 201):
                        return True
                    if y in range(450, 551):
                        help_screen()
                    if y in range(600, 701):
                        pygame.quit()
                        quit()
                if x in range(170, 371) and y in range(300, 401):
                    print("to white")
                    Board.player_color = "white"
                    Board.computer_color = "black"
                if x in range(470, 671) and y in range(300, 401):
                    print("switched")
                    Board.player_color = "black"
                    Board.computer_color = "white"
                    Oponent.computer.color = "white"


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


