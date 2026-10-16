import pygame

class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Fuentes
        self.font_btn = pygame.font.SysFont("Arial", 13, bold=True)
        self.font_status = pygame.font.SysFont("Arial", 15, bold=True)

        # Configuración de botones (Esquina superior derecha)
        btn_w, btn_h = 135, 30
        right_margin = width - 25
        x_pos = right_margin - btn_w

        self.rect_estilo1 = pygame.Rect(x_pos, 20, btn_w, btn_h)
        self.rect_estilo2 = pygame.Rect(x_pos, 58, btn_w, btn_h)
        self.rect_estilo3 = pygame.Rect(x_pos, 96, btn_w, btn_h)
        self.rect_reset   = pygame.Rect(x_pos, 134, btn_w, btn_h)

    def draw(self, screen, current_style, is_recording, is_frozen):
        # 1. Dibujar botones de control
        buttons = [
            (self.rect_estilo1, "Espectral", current_style == 1),
            (self.rect_estilo2, "Matrix", current_style == 2),
            (self.rect_estilo3, "Ecualizador", current_style == 3),
            (self.rect_reset,   "🔄 Reiniciar", False)
        ]

        for rect, label, active in buttons:
            bg_col = (0, 180, 216) if active else (5, 35, 55)
            border_col = (0, 245, 212)
            text_col = (10, 20, 30) if active else (0, 245, 212)

            pygame.draw.rect(screen, bg_col, rect, border_radius=15)
            pygame.draw.rect(screen, border_col, rect, 1, border_radius=15)

            txt_surf = self.font_btn.render(label, True, text_col)
            screen.blit(
                txt_surf, 
                (rect.x + (rect.width - txt_surf.get_width()) // 2, 
                 rect.y + (rect.height - txt_surf.get_height()) // 2)
            )

        # 2. Dibujar leyenda de estado inferior
        status_y = self.height - 35
        if is_recording:
            status_surf = self.font_status.render(
                f"🎙️ REGISTRANDO VOZ (ESTILO {current_style}) — ¡Habla fuerte!", True, (254, 228, 64)
            )
        elif is_frozen:
            status_surf = self.font_status.render(
                "✨ OBRA CONGELADA — Presiona [R] o Reiniciar para otra captura", True, (0, 245, 212)
            )
        else:
            status_surf = self.font_btn.render(
                "Captura tu firma de voz, tienes 3 segundos!", True, (0, 245, 212)
            )

        screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, status_y))