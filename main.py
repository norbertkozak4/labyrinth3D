import pygame
import sys
from game_states import GameStateManager
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, FULLSCREEN

def main():
    """Főprogram belépési pont"""
    pygame.init()
    pygame.mixer.init()
    
    # Ablak létrehozása
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Get actual screen dimensions and update constants
        import constants
        constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT = screen.get_size()
        constants.NUM_RAYS = constants.WINDOW_WIDTH  # Update rays for new width
    else:
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # F11 to toggle fullscreen
                    if FULLSCREEN:
                        screen = pygame.display.set_mode((1024, 768))
                        import constants
                        constants.FULLSCREEN = False
                        constants.WINDOW_WIDTH = 1024
                        constants.WINDOW_HEIGHT = 768
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        import constants
                        constants.FULLSCREEN = True
                        constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT = screen.get_size()
                    # Recreate game manager with new screen
                    game_manager = GameStateManager(screen)
                else:
                    game_manager.handle_event(event)
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
