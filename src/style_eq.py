import math
import random
import pygame

class EqualizerStyle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bars = []
        self.init_equalizer()

    def init_equalizer(self):
        self.bars = []
        num_bars = 90  
        total_width = self.width - 120
        bar_pitch = total_width / num_bars
        
        for i in range(num_bars):
            self.bars.append({
                'x': 60 + (i * bar_pitch),
                'width': max(2.0, bar_pitch * 0.55),
                'base_height': random.uniform(15, 50),
                'target_height': random.uniform(40, 240),
                'freq_offset': random.uniform(0.6, 2.8),
                'phase_shift': random.uniform(0, math.pi * 2)
            })

    def draw(self, screen, animation_time, smoothed_volume, is_frozen):
        screen.fill((1, 3, 8))
        
        horizon_y = self.height - 200
        center_x = self.width // 2
        
        # --- CREACIÓN DE LA CUADRÍCULA 3D CON BRILLO NEÓN ---
        # Creamos una superficie transparente para acumular el halo brillante del piso
        glow_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        grid_color_core = (120, 220, 255)  # Núcleo brillante celeste/blanco
        grid_color_glow = (0, 150, 255)  # Halo exterior cian/azul
        
        # 1. Líneas de perspectiva diagonales (con doble trazo para glow)
        for i in range(-7, 8):
            bottom_x = center_x + (i * 130)
            # Halo exterior difuminado (más grueso y transparente)
            pygame.draw.line(glow_surf, (*grid_color_glow, 45), (center_x, horizon_y), (bottom_x, self.height), 5)
            # Línea central nítida
            pygame.draw.line(glow_surf, (*grid_color_core, 180), (center_x, horizon_y), (bottom_x, self.height), 2)
            
        # 2. Líneas horizontales de profundidad
        for depth_step in range(1, 9):
            gy = horizon_y + (depth_step ** 1.7) * 9
            if gy < self.height:
                # Halo exterior horizontal
                pygame.draw.line(glow_surf, (*grid_color_glow, 45), (40, int(gy)), (self.width - 40, int(gy)), 5)
                # Línea central nítida horizontal
                pygame.draw.line(glow_surf, (*grid_color_core, 180), (40, int(gy)), (self.width - 40, int(gy)), 2)

        # Volcamos la capa de brillo del piso sobre la pantalla principal
        screen.blit(glow_surf, (0, 0))

        # Línea brillante de horizonte
        pygame.draw.line(screen, (0, 245, 212), (40, horizon_y), (WIDTH if 'WIDTH' in globals() else self.width - 40, horizon_y), 2)

        # --- DIBUJADO DE BARRAS DEL ECUALIZADOR ---
        for idx, bar in enumerate(self.bars):
            if not is_frozen:
                oscillation1 = math.sin(animation_time * (3.0 * bar['freq_offset']) + bar['phase_shift'])
                oscillation2 = math.cos(animation_time * 1.5 + (idx * 0.15))
                multibar_variation = (oscillation1 * 50.0) + (oscillation2 * 35.0)
                bar['target_height'] = 30.0 + (smoothed_volume * 250.0 * abs(math.sin(idx * 0.12 + animation_time))) + abs(multibar_variation)
                bar['base_height'] += (bar['target_height'] - bar['base_height']) * 0.25

            h = bar['base_height']
            x = bar['x']
            w = bar['width']

            ratio = idx / len(self.bars)
            if ratio < 0.33:
                bar_color = (0, 130, 255)  
            elif ratio < 0.66:
                bar_color = (0, 245, 212)  
            else:
                bar_color = (0, 255, 102)  

            pygame.draw.rect(screen, bar_color, (x, horizon_y - h, w, h))
            pygame.draw.rect(screen, (255, 255, 255), (x, horizon_y - h, w, 3))

            ref_surf = pygame.Surface((int(w), int(h * 0.35)), pygame.SRCALPHA)
            ref_surf.fill((*bar_color, 60))
            screen.blit(ref_surf, (x, horizon_y + 1))