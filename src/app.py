import pygame
import sys

from audio_manager import AudioManager
from ui_manager import UIManager
from input_handler import InputHandler
from style_spectral import SpectralStyle
from style_matrix import MatrixStyle
from style_eq import EqualizerStyle

class App:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.width, self.height = 1100, 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Eco Visual - Instalación Interactiva (Pygame Pro)")
        self.clock = pygame.time.Clock()

        # Fuentes
        self.font_matrix = pygame.font.SysFont("Courier", 14, bold=True)

        # Subsistemas y Estilos
        self.audio_mgr = AudioManager()
        self.audio_mgr.start()

        self.ui_mgr = UIManager(self.width, self.height)
        self.input_handler = InputHandler(self.ui_mgr)

        self.spectral_style = SpectralStyle(self.width, self.height)
        self.matrix_style = MatrixStyle(self.width, self.height, self.font_matrix)
        self.eq_style = EqualizerStyle(self.width, self.height)

        # Estados de la aplicación
        self.current_style = 1
        self.is_recording = False
        self.is_frozen = False
        self.animation_time = 0.0
        self.DURATION = 3.0

        self.frozen_wave_offset = 0.0
        self.frozen_amplitude_factor = 1.0

    def start_recording_sequence(self):
        if self.is_recording or self.is_frozen:
            return
        self.is_recording = True
        self.is_frozen = False
        print(f"\n[🎙️] Grabando voz por 3 segundos (Estilo {self.current_style})...")
        pygame.time.set_timer(pygame.USEREVENT, int(self.DURATION * 1000), 1)

    def finish_recording_sequence(self, smoothed_vol):
        if self.is_recording:
            self.is_recording = False
            self.is_frozen = True
            self.frozen_wave_offset = self.animation_time
            self.frozen_amplitude_factor = max(1.0, 1.0 + smoothed_vol * 0.9)
            print("[❄️] ¡Obra congelada con éxito en alta calidad!")

    def reset_installation(self):
        self.is_recording = False
        self.is_frozen = False
        self.matrix_style.init_rain()
        self.eq_style.init_equalizer()
        print("[🔄] Instalación reiniciada.")

    def set_style(self, style_num):
        if not self.is_recording:
            self.current_style = style_num
            self.reset_installation()
            print(f"[🎨] Estilo cambiado a: {style_num}")

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            smoothed_volume = self.audio_mgr.update()

            # Procesar eventos de temporizador
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.finish_recording_sequence(smoothed_volume)
                else:
                    pygame.event.post(event)

            # Manejo de entradas (teclado y mouse)
            running = self.input_handler.handle_events(
                on_space=self.start_recording_sequence,
                on_reset=self.reset_installation,
                on_set_style=self.set_style
            )
            if not running:
                break

            if not self.is_frozen:
                self.animation_time += 0.04

            # 1. Renderizado de la obra de arte activa
            if self.current_style == 1:
                self.spectral_style.draw(
                    self.screen, self.animation_time, smoothed_volume, 
                    self.is_frozen, self.frozen_wave_offset, self.frozen_amplitude_factor
                )
            elif self.current_style == 2:
                self.matrix_style.draw(self.screen, smoothed_volume, self.is_frozen)
            elif self.current_style == 3:
                self.eq_style.draw(self.screen, self.animation_time, smoothed_volume, self.is_frozen)

            # 2. Renderizado de la interfaz de usuario (botones y estados)
            self.ui_mgr.draw(self.screen, self.current_style, self.is_recording, self.is_frozen)

            pygame.display.flip()

        # Salida limpia
        self.audio_mgr.stop()
        pygame.quit()
        sys.exit()