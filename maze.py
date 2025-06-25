import random
from constants import MAP_SIZE

class Maze:
    """Labirintus generátor és kezelő osztály"""
    
    def __init__(self):
        self.grid = [[1 for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        self.start_pos = (1, 1)
        self.end_pos = (MAP_SIZE - 2, MAP_SIZE - 2)
        self.generate_maze()
    
    def generate_maze(self):
        """Labirintus generálása backtracking algoritmussal"""
        # Kezdeti állapot: minden fal
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                self.grid[y][x] = 1
        
        # Rekurzív backtracking
        self._carve_path(1, 1)
        
        # Kezdő és végpont biztosan üres
        self.grid[self.start_pos[1]][self.start_pos[0]] = 0
        self.grid[self.end_pos[1]][self.end_pos[0]] = 0
        
        # Végpont környékének tisztítása
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                y, x = self.end_pos[1] + dy, self.end_pos[0] + dx
                if 0 <= y < MAP_SIZE and 0 <= x < MAP_SIZE:
                    self.grid[y][x] = 0
    
    def _carve_path(self, x, y):
        """Út kivágása a labirintusban"""
        self.grid[y][x] = 0
        
        # Irányok véletlenszerű sorrendben
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Ellenőrizzük, hogy a cél pozíció a határon belül van-e
            if 1 <= nx < MAP_SIZE - 1 and 1 <= ny < MAP_SIZE - 1:
                # Ha a cél pozíció még fal
                if self.grid[ny][nx] == 1:
                    # Kivágás a cél pozíció irányába
                    self.grid[y + dy // 2][x + dx // 2] = 0
                    self._carve_path(nx, ny)
    
    def is_wall(self, x, y):
        """Ellenőrzi, hogy az adott pozíción fal van-e"""
        if x < 0 or x >= MAP_SIZE or y < 0 or y >= MAP_SIZE:
            return True
        return self.grid[int(y)][int(x)] == 1
    
    def get_cell(self, x, y):
        """Visszaadja az adott pozíció cellaértékét"""
        if x < 0 or x >= MAP_SIZE or y < 0 or y >= MAP_SIZE:
            return 1
        return self.grid[int(y)][int(x)]
    
    def get_start_position(self):
        """Kezdő pozíció"""
        return self.start_pos
    
    def get_end_position(self):
        """Cél pozíció"""
        return self.end_pos
