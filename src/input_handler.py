import pygame

class InputHandler:
    def __init__(self, ui_manager):
        self.ui = ui_manager

    def handle_events(self, on_space, on_reset, on_set_style):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    on_space()
                elif event.key == pygame.K_r:
                    on_reset()
                elif event.key == pygame.K_1:
                    on_set_style(1)
                elif event.key == pygame.K_2:
                    on_set_style(2)
                elif event.key == pygame.K_3:
                    on_set_style(3)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if self.ui.rect_estilo1.collidepoint((mx, my)):
                    on_set_style(1)
                elif self.ui.rect_estilo2.collidepoint((mx, my)):
                    on_set_style(2)
                elif self.ui.rect_estilo3.collidepoint((mx, my)):
                    on_set_style(3)
                elif self.ui.rect_reset.collidepoint((mx, my)):
                    on_reset()
                    
        return True