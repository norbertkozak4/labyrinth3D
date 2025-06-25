import pygame
import sys
from game_states import GameStateManager
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

def main():
    """Főprogram belépési pont"""
    pygame.init()
    pygame.mixer.init()
    
    # Ablak létrehozása
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Raycasting Labyrinth")
    clock = pygame.time.Clock()
    
    # Game state manager inicializálás
    game_manager = GameStateManager(screen)
    
    # Főciklus
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time másodpercben
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_manager.handle_event(event)
        
        # Update és render
        game_manager.update(dt)
        game_manager.render()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
