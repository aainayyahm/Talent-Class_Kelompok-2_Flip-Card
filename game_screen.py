# Kelompok 2
# 1. Ayla Ainayyah M
# 2. Aurora Ruth Praticia Sagala
# 3. Danita Divka Sajmira
# 4. Divana Taricha Salmalina
# 5. Ega Dwi Umadani
# 6. Dina Rahma Prasilda

import pygame as pg
import json
import random
from start_screen import start_screen

pg.init()

screen_width = 417
screen_height = 587
screen = pg.display.set_mode((screen_width, screen_height))
white = (255, 255, 255)

# Inisiasi scale
scale = 0.05

# Load images
background_img = pg.image.load("Assets/Background_General.png")

card_back_img = pg.image.load("Assets/card1.png")
card_open_img = pg.image.load("Assets/card2.png")
game_over_img = pg.image.load("Assets/game_over.png")
restart_button = pg.image.load("Assets/restart_button.png")  
win_img = pg.image.load("Assets/star3.png")  
back_button = pg.image.load("Assets/back_button.png")
shuffle_button = pg.image.load("Assets/shuffle_button.png")

# Mengubah ukuran images
background_img = pg.transform.smoothscale(background_img, (screen_width, screen_height))
game_over_img = pg.transform.smoothscale(game_over_img, (int(game_over_img.get_width() * scale), int(game_over_img.get_height() * scale)))
win_img = pg.transform.smoothscale(win_img, (int(win_img.get_width() * scale), int(win_img.get_height() * scale)))
restart_button = pg.transform.smoothscale(restart_button, (int(restart_button.get_width() * scale), int(restart_button.get_height() * scale)))
back_button = pg.transform.smoothscale(back_button, (int(back_button.get_width() * scale), int(back_button.get_height() * scale)))
shuffle_button = pg.transform.smoothscale(shuffle_button, (int(shuffle_button.get_width() * scale), int(shuffle_button.get_height() * scale)))
card_back_img = pg.transform.smoothscale(card_back_img, (int(card_back_img.get_width() * scale), int(card_back_img.get_height() * scale)))
card_open_img = pg.transform.smoothscale(card_open_img, (int(card_open_img.get_width() * scale), int(card_open_img.get_height() * scale)))

# Load music
sound_effect = pg.mixer.Sound("Assets/Lets Go.wav")
sound_effect.set_volume(0.5)
sound_effect.play(-1)

sound_lose = pg.mixer.Sound("Assets/Lose.wav")
sound_lose.set_volume(0.1)

sound_win = pg.mixer.Sound("Assets/Win.wav")
sound_win.set_volume(0.1)

sound_shuffle = pg.mixer.Sound("Assets/Shuffle.wav")
sound_shuffle.set_volume(1)

class WordCard:
    def __init__(self, word, name):
        self.word = word
        self.name = name
        self.is_face_up = False # Inisiasi kondisi kartu terbuka
        self.is_matched = False # Inisiasi kondisi kartu dengan kata yang sama

    def flip(self):
        self.is_face_up = not self.is_face_up

# Memanggil file Json
def load_card_contents(filename):
    with open(filename, 'r') as file:
        return json.load(file)

class WordGame:
    def __init__(self):
        self.cards = []
        self.load_cards(8)  # Inisiasi jumlah card yang dicocokkan
        self.start_time = pg.time.get_ticks()
        self.font = pg.font.SysFont('Arial', 15)
        self.bold_font = pg.font.SysFont('Arial', 18, bold=True)
        self.flipped_cards = []
        self.mismatch_timer = 0
        self.game_over = False  # Game over state
        self.win = False  # Win state
        self.is_music_playing = True

    # Kondisi untuk play background musik kecuali saat win dan game over
    def manage_background_music(self):
        if self.win or self.game_over:
            if self.is_music_playing:
                sound_effect.stop()
                self.is_music_playing = False
        else:
            if not self.is_music_playing:
                sound_effect.play(-1)  
                self.is_music_playing = True

    # Memanggil file Json
    def load_cards(self, number_of_pairs):
        contents = load_card_contents("Word.json")
        selected_contents = random.sample(contents, number_of_pairs)
        for content in selected_contents:
            card1 = WordCard(content['word'], content['name'])
            card2 = WordCard(content['word'], content['name'])
            self.cards.extend([card1, card2])
        random.shuffle(self.cards)
        
    def shuffle_cards(self):
            random.shuffle(self.cards)  # Mengacak posisi kartu
            for card in self.cards:
                card.is_face_up = False  # Tutup semua kartu yang terbuka
            self.flipped_cards = []  # Kosongkan daftar flipped cards
            self.mismatch_timer = 0
            sound_shuffle.play()
    
    def update(self):
        if not self.game_over and not self.win:
            elapsed_time = (pg.time.get_ticks() - self.start_time) / 1000  # Konversi ke detik
            self.time_remaining = max(0, 60 - int(elapsed_time))  # Update waktu ke 60 detik dan berkurang setiap detik
            if self.time_remaining <= 0:
                self.end_game()

            # Kondisi jika kartu tidak sama
            if len(self.flipped_cards) == 2:
                if self.flipped_cards[0].word != self.flipped_cards[1].word:
                    if self.mismatch_timer == 0:  
                        self.mismatch_timer = pg.time.get_ticks()
                else:
                    self.flipped_cards[0].is_matched = True
                    self.flipped_cards[1].is_matched = True
                    self.flipped_cards = []  

                    # Cek jika semua card sudah cocok
                    if all(card.is_matched for card in self.cards):
                        self.win = True  # Set win state
                        sound_win.play()
                        sound_effect.stop()

            if self.mismatch_timer != 0 and (pg.time.get_ticks() - self.mismatch_timer) > 1000:
                self.flipped_cards[0].flip()
                self.flipped_cards[1].flip()
                self.flipped_cards = []
                self.mismatch_timer = 0  # Reset timer
    
        self.manage_background_music()

    def end_game(self):
        self.game_over = True  # Set game over state
        print("Game Over")
        sound_lose.play()
        sound_effect.stop()

    def restart(self):
        self.cards = []
        self.stars_earned = 0
        self.time_remaining = 180
        self.load_cards(8)  # Jumlah kata yang harus dicocokkan
        self.start_time = pg.time.get_ticks()
        self.flipped_cards = []
        self.mismatch_timer = 0
        self.game_over = False  # Reset game over state
        self.win = False  # Reset win state

    def draw(self, screen):
        # Tampilan jika menang
        if self.win:
            screen.blit(win_img, (screen_width // 2 - win_img.get_width() // 2, screen_height // 2 - win_img.get_height() // 2))
            screen.blit(restart_button, (screen_width // 2, screen_height // 2.8 + game_over_img.get_height() // 2 + 10))
            screen.blit(back_button, (screen_width // 2 - back_button.get_width() - 10, screen_height // 2.8 + game_over_img.get_height() // 2 + 10))
            # screen.blit(restart_button, (screen_width // 2, screen_height // 2.8 + game_over_img.get_height() // 2))
            # screen.blit(back_button, (screen_width // 2 - back_button.get_width() - 10, screen_height // 2.8 + game_over_img.get_height() // 2))
        # Tampilan jika game over
        elif self.game_over:
            screen.blit(game_over_img, (screen_width // 2 - game_over_img.get_width() // 2, screen_height // 2 - game_over_img.get_height() // 2))
            screen.blit(restart_button, (screen_width // 2, screen_height // 2.8 + game_over_img.get_height() // 2 + 10))
            screen.blit(back_button, (screen_width // 2 - back_button.get_width() - 10, screen_height // 2.8 + game_over_img.get_height() // 2 + 10))
        else:
            # Untuk menampilkan cards
            cards_per_row = 4 # Jumlah kartu dalam 1 baris dan kolom
            for index, card in enumerate(self.cards):
                x = (index % cards_per_row) * (card_back_img.get_width() + 10) + 30
                y = (index // cards_per_row) * (card_back_img.get_height() + 10) + 70
                if card.is_face_up:
                    screen.blit(card_open_img, (x, y))
                    
                    # Menampilkan word dan name dari file Json
                    word_text = self.font.render(card.word, True, white)
                    name_text = self.font.render(card.name, True, white)
                    
                    screen.blit(word_text, (x + 15, y + 35))  
                    screen.blit(name_text, (x + 15, y + 55))   
                else:
                    screen.blit(card_back_img, (x, y))

            # Menampilkan waktu dan back button di game screen
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            timer_text = self.bold_font.render(f"{minutes:02}:{seconds:02}", True, (0, 0, 0))
            screen.blit(timer_text, (screen_width - 230, 20))
            screen.blit(back_button, (screen_width // 2 - 185, screen_height // 2.8 - 200))
            screen.blit(shuffle_button, (screen_width // 2 + 148, screen_height // 2.8 - 200))

def game_screen():
    pg.display.set_caption("Lontaraku Game")
    clock = pg.time.Clock()
    game = WordGame()
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Atur posisi mouse
                if game.win or game.game_over:
                    mouse_x, mouse_y = event.pos
                    restart_rect = pg.Rect(screen_width // 2, screen_height // 2.8 + game_over_img.get_height() // 2 + 10, restart_button.get_width(), restart_button.get_height())
                    if restart_rect.collidepoint(mouse_x, mouse_y):
                        game.restart()
                
                    back_rect = pg.Rect(screen_width // 2 - back_button.get_width() // 2 - back_button.get_width() - 10, screen_height // 2.8 + game_over_img.get_height() // 2 + 10, back_button.get_width(), back_button.get_height())
                    if back_rect.collidepoint(mouse_x, mouse_y):
                        return start_screen(game_screen)
                    
                    # sound_effect.stop()
                else:
                    mouse_x, mouse_y = event.pos
                    back_rect = pg.Rect(screen_width // 2 - 185, screen_height // 2.8 - 200, back_button.get_width(), back_button.get_height())
                    if back_rect.collidepoint(mouse_x, mouse_y):
                        return start_screen(game_screen)
                    
                    shuffle_rect = pg.Rect(screen_width // 2 + 148, screen_height // 2.8 - 200, shuffle_button.get_width(), shuffle_button.get_height())
                    if shuffle_rect.collidepoint(mouse_x, mouse_y):
                        game.shuffle_cards()

                    for index, card in enumerate(game.cards):
                        x = (index % 4) * (card_back_img.get_width() + 10) + 30
                        y = (index // 4) * (card_back_img.get_height() + 10) + 70

                        if x < mouse_x < x + card_back_img.get_width() and y < mouse_y < y + card_back_img.get_height():
                            if len(game.flipped_cards) < 2 and not card.is_face_up and not card.is_matched:  # Memastikan hanya 2 kartu yang bisa dibuka
                                card.flip()
                                game.flipped_cards.append(card)


        game.update()
        screen.fill(white)
        screen.blit(background_img, (0, 0))
        game.draw(screen)
        pg.display.flip()
        clock.tick(30)

    pg.quit()


if __name__ == "__main__":
    start_screen(game_screen)

