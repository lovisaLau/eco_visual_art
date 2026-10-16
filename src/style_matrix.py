import random
import pygame

class MatrixStyle:
    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        self.columns = []
        self.chars = "0101010101ABCDEFXYZ<>/*#@$%&"
        self.init_rain()

    def init_rain(self):
        self.columns = []
        col_width = 22
        num_cols = self.width // col_width
        for i in range(num_cols):
            self.columns.append({
                'x': i * col_width + 10,
                'y': random.uniform(-self.height, 0),
                'base_speed': random.uniform(3, 7),
                'chars': [random.choice(self.chars) for _ in range(25)]
            })

    def draw(self, screen, smoothed_volume, is_frozen):
        screen.fill((1, 12, 8))
        for col in self.columns:
            if not is_frozen:
                current_speed = col['base_speed'] + (smoothed_volume * 18.0)
                col['y'] += current_speed
                if col['y'] > self.height:
                    col['y'] = -400
                    col['chars'] = [random.choice(self.chars) for _ in range(25)]
            
            curr_y = col['y']
            for idx, char in enumerate(col['chars']):
                char_y = curr_y + (idx * 18)
                if 0 <= char_y <= self.height:
                    col_color = (255, 255, 255) if idx == 0 else ((0, 255, 102) if idx < 5 else (0, 143, 57))
                    txt_surface = self.font.render(char, True, col_color)
                    screen.blit(txt_surface, (col['x'], char_y))