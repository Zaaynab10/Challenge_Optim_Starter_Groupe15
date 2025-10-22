import numpy as np
import pygame

pygame.init()
font = pygame.font.SysFont('arial.ttf', 25)


# rgb colors
COLOR_MAP = [
    (0, 0, 0),
    (255, 255, 255),
    (30, 147, 255),
    (249, 60, 49),
    (79, 204, 48),
    (255, 220, 0),
    (229, 58, 163),
    (255, 133, 27)
]
BACKGROUND = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 5
SPEED = 40


class Game:
    def __init__(self, grid: np.array, title: str="Viewer", w=640, h=480, block_size: int=BLOCK_SIZE, template: bool=False):
        self._target = grid

        self.block_size = block_size
        self.active_mirror = template

        self.w = w
        self.h = h
        # init display
        self._display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()
        
        # init game state
        self.reset()
    
    def reset(self):
        self._grid = np.zeros_like(self._target)
        self._actions = []
        self._score = 0

    def play_step(self, action: str):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        # 5. update ui and clock
        self._actions.append(action)
        self._apply_action(action)
        self._update_ui()
        self._score = self.compute_score(self._grid)
        self._clock.tick(SPEED)
    
    def _update_ui(self):
        self._display.fill(BACKGROUND)
        for y in range(self._target.shape[0]):
            for x in range(self._target.shape[1]):
                if self.active_mirror:
                    pygame.draw.rect(self._display, COLOR_MAP[self._target[y][x]] or (0, 0, 0),
                                    pygame.Rect(x*self.block_size, y*self.block_size, self.block_size, self.block_size))
                    
                pygame.draw.rect(self._display, COLOR_MAP[self._grid[y][x]] or (0, 0, 0),
                                 pygame.Rect(x*self.block_size + (self.w//2 if self.active_mirror else 0), y*self.block_size, self.block_size, self.block_size))

        text_action = font.render(f"Actions: {len(self._actions)};            Epsilon: {0}", True, WHITE)
        text_score = font.render(f"Score: {self._score}", True, WHITE)
        self._display.blit(text_action, [0, 0])
        self._display.blit(text_score, [0, 20])
        pygame.display.flip()

    def _apply_action(self, action: str):
        """Applique une action RECT ou JOKER sur la grille."""
        parts = action.split()
        if parts[0] == "RECT":
            _, x1, y1, x2, y2, color = parts
            x1, y1, x2, y2, color = map(int, (x1, y1, x2, y2, color))
            self._grid[y1:y2+1, x1:x2+1] = color
        elif parts[0] == "JOKER":
            _, x1, y1, x2, y2 = parts
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
            self._grid[y1:y2+1, x1:x2+1] = self._target[y1:y2+1, x1:x2+1]
    
    def compute_score(self, current, max_actions: int=500):
        """Calcule le score à une étape donnée."""
        total_pixels = self._target.size
        correct_pixels = np.sum(self._target == current)

        if correct_pixels < total_pixels:
            return round(1_000_000 * correct_pixels / total_pixels)
        else:
            return round(1_000_000 * max_actions / len(self._actions))