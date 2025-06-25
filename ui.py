import pygame
from constants import *

class Button:
    """Egyszerű gomb osztály"""
    
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        self.is_clicked = False
        
    def handle_event(self, event):
        """Esemény kezelés"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False
        return False
    
    def render(self, screen):
        """Gomb rajzolása"""
        if self.is_clicked:
            color = BUTTON_CLICK_COLOR
        elif self.is_hovered:
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_COLOR
            
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Szöveg rajzolása
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class MenuState:
    """Főmenü állapot"""
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, FONT_SIZE * 2)
        
        # Get dynamic screen size
        screen_width = state_manager.screen.get_width()
        screen_height = state_manager.screen.get_height()
        
        # Gombok létrehozása
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = screen_height // 2
        
        self.start_button = Button(
            screen_width // 2 - button_width // 2,
            start_y,
            button_width, button_height,
            "Start Game", self.font
        )
        
        self.quit_button = Button(
            screen_width // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width, button_height,
            "Quit", self.font
        )
    
    def handle_event(self, event):
        """Esemény kezelés"""
        if self.start_button.handle_event(event):
            self.state_manager.change_state("game")
        elif self.quit_button.handle_event(event):
            pygame.quit()
            exit()
    
    def update(self, dt):
        """Frissítés"""
        pass
    
    def render(self, screen):
        """Renderelés"""
        screen.fill(BLACK)
        
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Cím
        title_text = self.title_font.render("Raycasting Labyrinth", True, WHITE)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))
        screen.blit(title_text, title_rect)
        
        # Gombok
        self.start_button.render(screen)
        self.quit_button.render(screen)
        
        # Irányítás leírása
        controls_text = [
            "Controls:",
            "WASD - Move",
            "Mouse - Look around",
            "ESC - Pause"
        ]
        
        y_offset = screen_height - 150
        for i, line in enumerate(controls_text):
            text_surface = self.font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset + i * 25))
            screen.blit(text_surface, text_rect)

class PauseState:
    """Szünet állapot"""
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, FONT_SIZE * 2)
        
        # Get dynamic screen size
        screen_width = state_manager.screen.get_width()
        screen_height = state_manager.screen.get_height()
        
        # Gombok létrehozása
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = screen_height // 2
        
        self.resume_button = Button(
            screen_width // 2 - button_width // 2,
            start_y,
            button_width, button_height,
            "Resume", self.font
        )
        
        self.menu_button = Button(
            screen_width // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width, button_height,
            "Main Menu", self.font
        )
        
        self.quit_button = Button(
            screen_width // 2 - button_width // 2,
            start_y + 2 * (button_height + button_spacing),
            button_width, button_height,
            "Quit", self.font
        )
    
    def handle_event(self, event):
        """Esemény kezelés"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state("game")
                return
        
        if self.resume_button.handle_event(event):
            self.state_manager.change_state("game")
        elif self.menu_button.handle_event(event):
            self.state_manager.change_state("menu")
        elif self.quit_button.handle_event(event):
            pygame.quit()
            exit()
    
    def update(self, dt):
        """Frissítés"""
        pass
    
    def render(self, screen):
        """Renderelés"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Félig átlátszó overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Cím
        title_text = self.title_font.render("PAUSED", True, WHITE)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))
        screen.blit(title_text, title_rect)
        
        # Gombok
        self.resume_button.render(screen)
        self.menu_button.render(screen)
        self.quit_button.render(screen)
