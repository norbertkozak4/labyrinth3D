import pygame
import math
import os
from constants import *

class RayCaster:
    """Raycasting engine"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Textúra betöltése
        self.wall_texture = self._load_texture("bush.png")
        
    def _load_texture(self, filename):
        """Textúra betöltése"""
        try:
            texture_path = os.path.join(os.path.dirname(__file__), filename)
            print(f"Textúra betöltése: {texture_path}")
            texture = pygame.image.load(texture_path).convert()
            print(f"Textúra sikeresen betöltve: {texture.get_width()}x{texture.get_height()}")
            return texture
        except pygame.error as e:
            print(f"Nem sikerült betölteni a textúrát {filename}: {e}")
            # Fallback: egyszerű színes surface
            fallback = pygame.Surface((64, 64))
            fallback.fill(GREEN)
            return fallback
        
    def cast_rays(self, player, maze):
        """Sugarak kilövése és 3D nézet renderelése"""
        # Plafon és talaj renderelése
        self._draw_floor_ceiling()
        
        # FOV számítás
        fov_rad = math.radians(FOV)
        ray_angle_step = fov_rad / self.screen_width
        start_angle = player.angle - fov_rad / 2
        
        for i in range(self.screen_width):
            ray_angle = start_angle + i * ray_angle_step
            
            # Sugár kilövése
            ray_result = self._cast_single_ray(player.x, player.y, ray_angle, maze)
            distance, wall_x = ray_result
            
            # Perspektívikus korrekció
            distance = distance * math.cos(ray_angle - player.angle)
            
            # Fal magasság számítása
            if distance > 0:
                wall_height = (WALL_HEIGHT * self.screen_height) / distance
                wall_top = (self.screen_height - wall_height) / 2
                wall_bottom = wall_top + wall_height
                
                # Textúra koordináta számítása
                texture_x = int(wall_x * self.wall_texture.get_width()) % self.wall_texture.get_width()
                
                # Távolság alapú árnyékolás
                color_intensity = max(0.3, min(1.0, 1.0 - distance / (MAP_SIZE * CELL_SIZE * 0.7)))
                
                # Textúrázott fal rajzolása
                self._draw_textured_wall(i, wall_top, wall_bottom, texture_x, color_intensity)
    
    def _draw_textured_wall(self, screen_x, wall_top, wall_bottom, texture_x, color_intensity):
        """Textúrázott fal rajzolása"""
        wall_height = wall_bottom - wall_top
        texture_height = self.wall_texture.get_height()
        
        # Ha a fal túl kicsi, egyszerű vonal rajzolása
        if wall_height < 1:
            return
            
        # Textúra koordináták korrekciója
        texture_x = max(0, min(int(texture_x), self.wall_texture.get_width() - 1))
        
        try:
            # Textúra oszlop kivágása (1 pixel széles csík)
            column_rect = pygame.Rect(texture_x, 0, 1, texture_height)
            column_surface = self.wall_texture.subsurface(column_rect).copy()
            
            # Méretezés a fal magasságára
            wall_height_int = max(1, int(wall_height))
            if wall_height_int != texture_height:
                column_surface = pygame.transform.scale(column_surface, (1, wall_height_int))
            
            # Árnyékolás ideiglenesen kikapcsolva a hibakereséshez
            # TODO: Árnyékolás implementálása később
            
            # Oszlop rajzolása a képernyőre
            self.screen.blit(column_surface, (screen_x, int(wall_top)))
            
        except Exception as e:
            # Fallback: egyszerű színes vonal (ha textúra betöltés nem sikerült)
            print(f"Textúra rajzolási hiba: {e}")
            color = (int(GREEN[0] * color_intensity), int(GREEN[1] * color_intensity), int(GREEN[2] * color_intensity))
            pygame.draw.line(self.screen, color, (screen_x, int(wall_top)), (screen_x, int(wall_bottom)))
    
    def _draw_floor_ceiling(self):
        """Talaj és plafon rajzolása"""
        # Plafon (felső fél)
        pygame.draw.rect(
            self.screen,
            BLUE,
            (0, 0, self.screen_width, self.screen_height // 2)
        )
        
        # Talaj (alsó fél)
        pygame.draw.rect(
            self.screen,
            BROWN,
            (0, self.screen_height // 2, self.screen_width, self.screen_height // 2)
        )
    
    def _cast_single_ray(self, start_x, start_y, angle, maze):
        """Egyetlen sugár kilövése"""
        dx = math.cos(angle)
        dy = math.sin(angle)
        
        # DDA algoritmus
        map_x = int(start_x // CELL_SIZE)
        map_y = int(start_y // CELL_SIZE)
        
        # Következő grid vonal távolsága
        if dx == 0:
            delta_dist_x = float('inf')
        else:
            delta_dist_x = abs(1 / dx) * CELL_SIZE
            
        if dy == 0:
            delta_dist_y = float('inf')
        else:
            delta_dist_y = abs(1 / dy) * CELL_SIZE
        
        # Lépés irány kiszámítása
        if dx < 0:
            step_x = -1
            side_dist_x = (start_x / CELL_SIZE - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - start_x / CELL_SIZE) * delta_dist_x
            
        if dy < 0:
            step_y = -1
            side_dist_y = (start_y / CELL_SIZE - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - start_y / CELL_SIZE) * delta_dist_y
        
        # DDA
        hit = False
        side = 0  # 0 ha NS fal, 1 ha EW fal
        
        while not hit:
            # Következő grid vonal
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1
            
            # Falba ütköztünk?
            if maze.is_wall(map_x, map_y):
                hit = True
        
        # Távolság számítása
        if side == 0:
            perp_wall_dist = (map_x - start_x / CELL_SIZE + (1 - step_x) / 2) / dx
        else:
            perp_wall_dist = (map_y - start_y / CELL_SIZE + (1 - step_y) / 2) / dy
        
        # Fal ütközési pont számítása textúra koordinátákhoz
        if side == 0:
            wall_x = start_y / CELL_SIZE + perp_wall_dist * dy
        else:
            wall_x = start_x / CELL_SIZE + perp_wall_dist * dx
        wall_x = wall_x - math.floor(wall_x)  # Tört rész (0-1 között)
        
        return abs(perp_wall_dist * CELL_SIZE), wall_x
