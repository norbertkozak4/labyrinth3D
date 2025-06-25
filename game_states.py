import pygame
import math
from maze import Maze
from player import Player
from raycaster import RayCaster
from ui import MenuState, PauseState
from constants import *

class GameState:
    """Játék állapot"""
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font = pygame.font.Font(None, FONT_SIZE)
        
        # Játék komponensek
        self.maze = Maze()
        start_x, start_y = self.maze.get_start_position()
        self.player = Player(start_x, start_y)
        self.player.set_maze(self.maze)
        self.raycaster = RayCaster(state_manager.screen)
        
        # Játék állapot
        self.game_won = False
        self.win_time = 0
    
    def handle_event(self, event):
        """Esemény kezelés"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state("pause")
                self.player.reset_mouse()
    
    def update(self, dt):
        """Frissítés"""
        if self.game_won:
            self.win_time += dt
            if self.win_time > 3.0:  # 3 másodperc után vissza a menübe
                self.state_manager.change_state("menu")
            return
        
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
        
        # Nyerés ellenőrzése
        player_map_pos = self.player.get_map_position()
        end_pos = self.maze.get_end_position()
        
        if player_map_pos == end_pos:
            self.game_won = True
            self.win_time = 0
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
    
    def render(self, screen):
        """Renderelés"""
        # 3D nézet
        self.raycaster.cast_rays(self.player, self.maze)
        
        # Minimap (opcionális)
        self._draw_minimap(screen)
        
        # Nyerés üzenet
        if self.game_won:
            self._draw_win_message(screen)
    
    def _draw_minimap(self, screen):
        """Minimap rajzolása"""
        screen_width = screen.get_width()
        minimap_size = 150
        cell_size = minimap_size // MAP_SIZE
        minimap_x = screen_width - minimap_size - 10
        minimap_y = 10
        
        # Háttér
        pygame.draw.rect(screen, DARK_GRAY, 
                        (minimap_x - 5, minimap_y - 5, minimap_size + 10, minimap_size + 10))
        
        # Labirintus
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                color = WHITE if self.maze.get_cell(x, y) == 1 else BLACK
                pygame.draw.rect(screen, color,
                               (minimap_x + x * cell_size, minimap_y + y * cell_size,
                                cell_size, cell_size))
        
        # Cél pozíció (zöld kör)
        end_x, end_y = self.maze.get_end_position()
        pygame.draw.circle(screen, GREEN,
                          (minimap_x + end_x * cell_size + cell_size // 2,
                           minimap_y + end_y * cell_size + cell_size // 2),
                          max(2, cell_size // 4))
        
        # Játékos pozíció és irány
        player_map_x, player_map_y = self.player.get_map_position()
        player_center_x = minimap_x + player_map_x * cell_size + cell_size // 2
        player_center_y = minimap_y + player_map_y * cell_size + cell_size // 2
        
        # Játékos pozíció (piros kör)
        pygame.draw.circle(screen, RED, (player_center_x, player_center_y), max(2, cell_size // 4))
        
        # Játékos nézési irány (vonal)
        direction_length = cell_size // 2
        end_x = player_center_x + math.cos(self.player.angle) * direction_length
        end_y = player_center_y + math.sin(self.player.angle) * direction_length
        pygame.draw.line(screen, RED, (player_center_x, player_center_y), (end_x, end_y), 2)
    
    def _draw_win_message(self, screen):
        """Nyerés üzenet rajzolása"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        win_text = self.font.render("Congratulations! You've escaped the maze!", True, WHITE)
        win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(win_text, win_rect)
        
        return_text = self.font.render("Returning to menu...", True, WHITE)
        return_rect = return_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(return_text, return_rect)
    
    def reset_game(self):
        """Játék újraindítása"""
        self.maze = Maze()
        start_x, start_y = self.maze.get_start_position()
        self.player = Player(start_x, start_y)
        self.player.set_maze(self.maze)
        self.game_won = False
        self.win_time = 0
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

class GameStateManager:
    """Játék állapot kezelő"""
    
    def __init__(self, screen):
        self.screen = screen
        self.states = {}
        self.current_state = None
        
        # Állapotok létrehozása
        self.states["menu"] = MenuState(self)
        self.states["game"] = GameState(self)
        self.states["pause"] = PauseState(self)
        
        # Kezdő állapot
        self.change_state("menu")
    
    def change_state(self, state_name):
        """Állapot váltás"""
        if state_name in self.states:
            # Egér láthatóság beállítása állapot szerint
            if state_name in ["menu", "pause"]:
                # Menükben látható az egér
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            elif state_name == "game":
                # Játékban rejtett az egér
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
                if self.current_state != "pause":  # Ha nem pause-ból jövünk, új játék
                    self.states["game"].reset_game()
                else:  # Ha pause-ból jövünk, folytatás
                    self.states["game"].player.reset_mouse()
            
            self.current_state = state_name
    
    def handle_event(self, event):
        """Esemény kezelés"""
        if self.current_state in self.states:
            self.states[self.current_state].handle_event(event)
    
    def update(self, dt):
        """Frissítés"""
        if self.current_state in self.states:
            self.states[self.current_state].update(dt)
    
    def render(self):
        """Renderelés"""
        if self.current_state in self.states:
            self.states[self.current_state].render(self.screen)
