import math
import random
import pygame

class SpectralStyle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bg_stars = []
        self.corner_origins = [(0, 0), (width, 0), (width, height), (0, height)]
        self.init_stars()

    def init_stars(self):
        self.bg_stars = []
        for _ in range(100):
            cx, cy = random.choice(self.corner_origins)
            angle = math.atan2((self.height/2) - cy, (self.width/2) - cx) + random.uniform(-1.0, 1.0)
            speed = random.uniform(0.3, 1.2)
            self.bg_stars.append({
                'x': float(cx + random.uniform(-50, 50)),
                'y': float(cy + random.uniform(-50, 50)),
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.uniform(1.2, 2.8),
                'color': random.choice([(255, 42, 133), (0, 180, 216), (82, 183, 136), (255, 255, 255), (254, 228, 64)])
            })

    def get_color_rgb(self, nx):
        if nx < -0.2:
            t = (nx - (-1.0)) / 0.8
            r = int(255 * (1 - t) + 0 * t)
            g = int(42 * (1 - t) + 180 * t)
            b = int(133 * (1 - t) + 216 * t)
        elif nx < 0.4:
            t = (nx - (-0.2)) / 0.6
            r = int(0 * (1 - t) + 82 * t)
            g = int(180 * (1 - t) + 183 * t)
            b = int(216 * (1 - t) + 136 * t)
        else:
            t = (nx - 0.4) / 0.6
            t = max(0.0, min(1.0, t))
            r = int(82 * (1 - t) + 210 * t)
            g = int(183 * (1 - t) + 230 * t)
            b = int(136 * (1 - t) + 50 * t)
        return (r, g, b)

    def draw(self, screen, animation_time, smoothed_volume, is_frozen, frozen_offset, frozen_amp):
        
        # Limpiar la pantalla por completo con el fondo opaco para evitar rastros de otros modos
        screen.fill((2, 4, 8))
    
        
        # Fondo y brillos atmosféricos
        surf_glow = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(surf_glow, (24, 3, 36, 120), (-100, 50, int(self.width * 0.5), self.height - 100))
        pygame.draw.ellipse(surf_glow, (2, 24, 54, 120), (int(self.width * 0.25), 0, int(self.width * 0.5), self.height))
        pygame.draw.ellipse(surf_glow, (3, 38, 30, 120), (int(self.width * 0.5), 50, int(self.width * 0.5), self.height - 100))
        screen.blit(surf_glow, (0, 0))

        # Estrellas de fondo
        for star in self.bg_stars:
            star['x'] += star['vx']
            star['y'] += star['vy']
            if (self.width * 0.2 < star['x'] < self.width * 0.8) and (self.height * 0.1 < star['y'] < self.height * 0.9):
                if random.random() < 0.025:
                    cx, cy = random.choice(self.corner_origins)
                    angle = math.atan2((self.height/2) - cy, (self.width/2) - cx) + random.uniform(-1.0, 1.0)
                    speed = random.uniform(0.3, 1.2)
                    star['x'] = float(cx)
                    star['y'] = float(cy)
                    star['vx'] = math.cos(angle) * speed
                    star['vy'] = math.sin(angle) * speed
            pygame.draw.circle(screen, star['color'], (int(star['x']), int(star['y'])), star['size'])

        center_y = self.height // 2 + 20
        num_layers = 64
        t_base = frozen_offset if is_frozen else animation_time
        amp_factor = frozen_amp if is_frozen else (1.0 + smoothed_volume * 1.8)

        for l in range(num_layers):
            step = 8
            points = []
            for x in range(0, self.width + step, step):
                nx = (x - self.width / 2) / (self.width / 2)
                envelope = max(0.0, 1.0 - nx**4)
                w1 = math.sin(x * 0.007 + t_base + (l * 0.07))
                w2 = math.sin(x * 0.013 - t_base * 1.3 + (l * 0.04)) * 0.6
                w3 = math.cos(x * 0.003 + t_base * 0.6 + (l * 0.08)) * 0.4
                w4 = math.sin(x * 0.022 + t_base * 0.8) * 0.2
                y_offset = (w1 + w2 + w3 + w4) * 65.0 * amp_factor * envelope
                layer_spread = (l - num_layers / 2) * 0.95
                y = center_y + y_offset + layer_spread
                points.append((x, y))

            for s in range(len(points) - 1):
                x1, y1 = points[s]
                x2, y2 = points[s + 1]
                mid_x = (x1 + x2) / 2
                nx_mid = (mid_x - self.width / 2) / (self.width / 2)
                col = self.get_color_rgb(nx_mid)
                pygame.draw.aaline(screen, col, (x1, y1), (x2, y2))