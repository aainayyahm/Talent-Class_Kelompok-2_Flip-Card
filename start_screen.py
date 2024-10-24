import pygame as pg
import sys
# from game_screen import game_screen

def start_screen(game_function):
    pg.init()

    screen_width = 417
    screen_height = 587
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Lontaraku Game")

    button_scale = 0.5

    welcome_img = pg.image.load("Assets/Background_Welcome.jpg")
    welcome_img = pg.transform.smoothscale(welcome_img, (screen_width, screen_height))

    button_img = pg.image.load("Assets/start_button.png") 
    button_img = pg.transform.smoothscale(button_img, (int(button_img.get_width() * button_scale), int(button_img.get_height() * button_scale)))
    button_rect = button_img.get_rect(center = (screen_width // 2, screen_height // 1.8))

    run = True
    while run:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and button_rect.collidepoint(event.pos):
                        game_function()  
                        return  
        
        screen.fill((255,255,255))
        screen.blit(welcome_img, (0,0))
        screen.blit(button_img, button_rect) 

        pg.display.update()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    from game_screen import game_screen  
    start_screen(game_screen) 