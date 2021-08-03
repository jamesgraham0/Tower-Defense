import pygame

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((900, 700))
    from menus.main_menu import MainMenu
    mainMenu = MainMenu(win)
    mainMenu.run()