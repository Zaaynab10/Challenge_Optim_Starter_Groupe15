import numpy as np
import pygame
from figure import Figure
from collections import deque # Pour la fonction de composantes connexes
import random


pygame.init()
font = pygame.font.SysFont('arial.ttf', 25)


# rgb colors
COLOR_MAP = {
    0: (0, 0, 0),           # Noir
    1: (255, 255, 255),     # Rouge
    2: (30, 147, 255),      # Vert
    3: (249, 60, 49),       # Bleu
    4: (79, 204, 48),       # Jaune
    5: (255, 220, 0),       # Magenta
    6: (229, 58, 163),      # Cyan
    7: (255, 133, 27)       # Gris
}
BACKGROUND = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 60
NUM_TOP_ZONES = 3

class GameEnv:
    def __init__(self, figure: Figure, title: str="Viewer", w=640, h=480, block_size: int=BLOCK_SIZE, clone: bool=False, show: bool=True):
        self.figure = figure
        self._target = figure.grid
        self.block_size = block_size
        self.active_mirror = clone
        self.w = w
        self.h = h

        self.max_jokers_allowed = figure.maxJokers
        self.max_joker_rect_size = figure.maxJokerSize

        self.show = show
        if self.show == True:
            grid_height, grid_width = self._target.shape
            display_width = grid_width * self.block_size * (2 if self.active_mirror else 1)
            display_height = grid_height * self.block_size + 40
            self._display = pygame.display.set_mode((max(self.w, display_width), max(self.h, display_height)))
            pygame.display.set_caption(title)
            self._clock = pygame.time.Clock()

        self.reset()
        # NOUVEAU: Espace d'actions étendu
        # (NUM_TOP_ZONES zones * (8 couleurs + 1 joker)) + 1 (pour NO_OP si aucune zone)
        self.n_actions = NUM_TOP_ZONES * (len(COLOR_MAP) + 1) + 1 # +1 pour NO_OP
        self._zone_pool = []


    def _find_connected_components(self, grid):
        rows, cols = grid.shape
        visited = np.zeros_like(grid, dtype=bool)
        zones = []
        zone_id_counter = 0

        for r in range(rows):
            for c in range(cols):
                if not visited[r, c]:
                    zone_id_counter += 1
                    target_color = grid[r, c]
                    current_zone_pixels = []
                    min_r, max_r = r, r
                    min_c, max_c = c, c

                    q = deque([(r, c)])
                    visited[r, c] = True

                    while q:
                        curr_r, curr_c = q.popleft()
                        current_zone_pixels.append((curr_r, curr_c))

                        min_r = min(min_r, curr_r)
                        max_r = max(max_r, curr_r)
                        min_c = min(min_c, curr_c)
                        max_c = max(max_c, curr_c)

                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = curr_r + dr, curr_c + dc
                            if (0 <= nr < rows and 0 <= nc < cols and
                                not visited[nr, nc] and grid[nr, nc] == target_color):
                                visited[nr, nc] = True
                                q.append((nr, nc))

                    zones.append({
                        'id': zone_id_counter,
                        'color': target_color,
                        'pixels': current_zone_pixels,
                        'bbox': (min_c, min_r, max_c, max_r), # (x1, y1, x2, y2)
                        'size': len(current_zone_pixels)
                    })
        return zones

    def reset(self):
        self._grid = np.zeros_like(self._target)
        self._actions_history = []
        self._total_jokers_used = 0
        self._score = 0
        self._frame_iteration = 0
        self._zone_pool = []

        self._target_zones = self._find_connected_components(self._target)
        self._target_zones.sort(key=lambda z: z['size'], reverse=True)


    def play_step(self, action_idx: int):
        self._frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        reward = -0.5 # Pénalité par défaut plus faible pour encourager l'exploration

        action_status = self._apply_agent_action(action_idx)

        if action_status == "invalid_action":
            reward -= 9.5 # Pénalité modérée pour permettre l'exploration de zones
        elif action_status == "no_op":
            reward -= 3.5 # Pénalité douce pour une non-action
        elif action_status == "joker_applied":
            reward += 20 # Récompense un peu plus grande pour un joker bien utilisé

        self._update_ui()
        previous_score = self._score
        self._score = self.compute_score(self._grid)

        reward += (self._score - previous_score) / 1000 # Normaliser la récompense de score

        game_over = False
        if np.array_equal(self._grid, self._target):
            reward += 1000
            game_over = True
        elif len(self._actions_history) >= self.figure.maxActions:
            reward -= 500
            game_over = True
        elif self._frame_iteration > self.figure.maxActions * 2:
            reward -= 200
            game_over = True

        if self.show:
            self._clock.tick(SPEED)

        return reward, game_over, self._score

    def _get_uncolored_zones(self):
        return [zone for zone in self._target_zones if not np.array_equal(
            self._grid[zone['bbox'][1]:zone['bbox'][3]+1, zone['bbox'][0]:zone['bbox'][2]+1],
            self._target[zone['bbox'][1]:zone['bbox'][3]+1, zone['bbox'][0]:zone['bbox'][2]+1]
        )]

    def _prepare_zone_pool(self):
        uncolored_zones = self._get_uncolored_zones()
        if not uncolored_zones:
            self._zone_pool = []
            return self._zone_pool

        if len(uncolored_zones) <= NUM_TOP_ZONES:
            self._zone_pool = uncolored_zones.copy()
        else:
            # Mélange pour varier les zones proposées tout en gardant un sous-ensemble fixe
            sampled = random.sample(uncolored_zones, NUM_TOP_ZONES)
            sampled.sort(key=lambda z: z['size'], reverse=True)
            self._zone_pool = sampled
        return self._zone_pool

    def _update_ui(self):
        if not self.show: return
        self._display.fill(BACKGROUND)
        for y in range(self._target.shape[0]):
            for x in range(self._target.shape[1]):
                if self.active_mirror:
                    pygame.draw.rect(self._display, COLOR_MAP.get(self._target[y][x], (0,0,0)),
                                     pygame.Rect(x*self.block_size, y*self.block_size, self.block_size, self.block_size))

                target_x_offset = (self.w // 2 if self.active_mirror else 0)
                pygame.draw.rect(self._display, COLOR_MAP.get(self._grid[y][x], (0,0,0)),
                                 pygame.Rect(x*self.block_size + target_x_offset, y*self.block_size, self.block_size, self.block_size))

        text_action = font.render(f"Actions: {len(self._actions_history)}; Jokers: {self._total_jokers_used}/{self.max_jokers_allowed}", True, WHITE)
        text_score = font.render(f"Score: {self._score}", True, WHITE)
        self._display.blit(text_action, [0, 0])
        self._display.blit(text_score, [0, 20])
        pygame.display.flip()

    def _apply_agent_action(self, action_idx: int):
        """
        Interprète l'action numérique de l'agent et l'applique.
        action_idx: Index de l'action dans l'espace étendu.
        """
        if not self._zone_pool:
            self._prepare_zone_pool()
        zone_pool = self._zone_pool

        # NOUVEAU: Gérer l'action "NO_OP"
        if action_idx == self.n_actions - 1: # Si c'est la dernière action possible (NO_OP)
            if not zone_pool: # Si vraiment rien à faire
                self._actions_history.append("NO_OP")
                return "no_op"
            else: # Si l'agent choisit NO_OP alors qu'il y a des choses à faire
                self._actions_history.append("INVALID_NO_OP")
                return "invalid_action"

        if not zone_pool:
            self._actions_history.append("NO_OP_NO_ZONE")
            return "no_op" # Rien à colorier, mais ce n'est pas une action de l'agent

        # NOUVEAU: Choisir la zone à cibler
        zone_action_space_size = len(COLOR_MAP) + 1 # 8 couleurs + 1 joker
        target_zone_idx = action_idx // zone_action_space_size
        color_or_joker_action = action_idx % zone_action_space_size

        if target_zone_idx >= len(zone_pool):
            # L'agent a choisi une zone en dehors du sous-ensemble proposé
            self._actions_history.append(f"INVALID_ZONE_SELECTION {action_idx}")
            return "invalid_action"

        target_zone = zone_pool[target_zone_idx]
        x1, y1, x2, y2 = target_zone['bbox']

        if color_or_joker_action < len(COLOR_MAP): # C'est une action RECT
            color = color_or_joker_action
            self._grid[y1:y2+1, x1:x2+1] = color
            self._actions_history.append(f"RECT {x1} {y1} {x2} {y2} {color}")
            self._zone_pool = []
            return "rect_applied"
        elif color_or_joker_action == len(COLOR_MAP): # C'est une action JOKER
            width = x2 - x1 + 1
            height = y2 - y1 + 1

            if (self._total_jokers_used >= self.max_jokers_allowed or
                width * height > self.max_joker_rect_size):
                self._actions_history.append(f"INVALID_JOKER {x1} {y1} {x2} {y2}")
                return "invalid_action"

            self._grid[y1:y2+1, x1:x2+1] = self._target[y1:y2+1, x1:x2+1]
            self._total_jokers_used += 1
            self._actions_history.append(f"JOKER {x1} {y1} {x2} {y2}")
            self._zone_pool = [] # Recalculer après un changement majeur
            return "joker_applied"
        else:
            self._actions_history.append(f"UNKNOWN_ACTION_DETAIL {action_idx}")
            return "invalid_action"


    def compute_score(self, current):
        total_pixels = self._target.size
        correct_pixels = np.sum(self._target == current)

        if correct_pixels < total_pixels:
            return round(1_000_000 * correct_pixels / total_pixels)
        else:
            return round(1_000_000 * self.figure.maxActions / len(self._actions_history))

    def get_state(self):
        """Encode l'état courant pour le DQN (grilles + zones + infos globales)."""
        # --- Vue complète de la fresque ---
        current_flat = (self._grid.astype(np.float32).flatten()) / 7.0
        target_flat = (self._target.astype(np.float32).flatten()) / 7.0
        diff_flat = (self._grid != self._target).astype(np.float32).flatten()

        zone_pool = self._prepare_zone_pool()

        zone_features = []
        for i in range(NUM_TOP_ZONES):
            if i < len(zone_pool):
                target_zone = zone_pool[i]
                x1, y1, x2, y2 = target_zone['bbox']
                zone_width = x2 - x1 + 1
                zone_height = y2 - y1 + 1

                zone_features.extend([
                    target_zone['color'] / 7.0,
                    target_zone['size'] / self._target.size,
                    x1 / self._target.shape[1],
                    y1 / self._target.shape[0],
                    zone_width / self._target.shape[1],
                    zone_height / self._target.shape[0],
                ])
            else:
                zone_features.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        # --- Indicateurs globaux ---
        max_actions = max(1, self.figure.maxActions)
        max_jokers_allowed = max(1, self.max_jokers_allowed)
        global_features = [
            len(self._actions_history) / max_actions,
            self._total_jokers_used / max_jokers_allowed if self.max_jokers_allowed > 0 else 0.0,
            1.0 if np.array_equal(self._grid, self._target) else 0.0,
        ]

        state = np.concatenate([
            current_flat,
            target_flat,
            diff_flat,
            np.array(zone_features, dtype=np.float32),
            np.array(global_features, dtype=np.float32),
        ]).astype(np.float32)
        return state