import pygame
import math
from constants import *

class Player:
    """Játékos osztály"""
    
    def __init__(self, x, y, angle=0):
        self.x = x * CELL_SIZE + CELL_SIZE // 2
        self.y = y * CELL_SIZE + CELL_SIZE // 2
        self.angle = angle
        self.maze = None
        
        # Mouse control
        self.mouse_sensitivity = 0.002
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
    def set_maze(self, maze):
        """Labirintus referencia beállítása"""
        self.maze = maze
    
    def update(self, dt, keys):
        """Játékos frissítése"""
        if not self.maze:
            return
            
        # Mouse fordulás
        mouse_rel = pygame.mouse.get_rel()
        self.angle += mouse_rel[0] * self.mouse_sensitivity
        
        # Mozgás számítása
        dx = dy = 0
        
        if keys[pygame.K_w]:  # Előre
            dx += math.cos(self.angle) * PLAYER_SPEED * dt
            dy += math.sin(self.angle) * PLAYER_SPEED * dt
        
        if keys[pygame.K_s]:  # Hátra
            dx -= math.cos(self.angle) * PLAYER_SPEED * dt
            dy -= math.sin(self.angle) * PLAYER_SPEED * dt
        
        if keys[pygame.K_a]:  # Balra (strafe)
            dx += math.cos(self.angle - math.pi/2) * PLAYER_SPEED * dt
            dy += math.sin(self.angle - math.pi/2) * PLAYER_SPEED * dt
        
        if keys[pygame.K_d]:  # Jobbra (strafe)
            dx += math.cos(self.angle + math.pi/2) * PLAYER_SPEED * dt
            dy += math.sin(self.angle + math.pi/2) * PLAYER_SPEED * dt
        
        # Ütközésvizsgálat és mozgás
        self._move_with_collision(dx, dy)
    
    def _move_with_collision(self, dx, dy):
        """Mozgás ütközésvizsgálattal"""
        # X irányú mozgás
        new_x = self.x + dx
        map_x = int(new_x // CELL_SIZE)
        map_y = int(self.y // CELL_SIZE)
        
        if not self.maze.is_wall(map_x, map_y):
            self.x = new_x
        
        # Y irányú mozgás
        new_y = self.y + dy
        map_x = int(self.x // CELL_SIZE)
        map_y = int(new_y // CELL_SIZE)
        
        if not self.maze.is_wall(map_x, map_y):
            self.y = new_y
    
    def get_position(self):
        """Pozíció lekérdezése"""
        return self.x, self.y
    
    def get_map_position(self):
        """Térkép pozíció lekérdezése"""
        return int(self.x // CELL_SIZE), int(self.y // CELL_SIZE)
    
    def reset_mouse(self):
        """Egér resetelése (például játék szüneteltetésekor)"""
        pygame.mouse.get_rel()  # Eldobja az akkumulált mouse mozgást
