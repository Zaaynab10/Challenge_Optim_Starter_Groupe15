import json
import test_solution
import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib

def solve_M_Chat_contour_optimal(dataset_txt):
    """Contour bleu décomposé en formes géométriques optimales"""
    solution = """RECT 0 0 99 99 6
# ÉTAPE 1: Carré central du visage
RECT 35 25 65 45 2

# ÉTAPE 2: Oreille gauche (triangle)
RECT 25 15 40 30 2

# ÉTAPE 3: Oreille droite (triangle)  
RECT 60 15 75 30 2

# ÉTAPE 4: Menton arrondi (forme en D)
RECT 30 40 70 50 2

# ÉTAPE 5: Affinage du menton
RECT 25 45 75 48 2

# ÉTAPE 6: Yeux noirs
RECT 40 30 45 35 0
RECT 55 30 60 35 0

# ÉTAPE 7: Nez rouge
RECT 48 38 52 42 5

# ÉTAPE 8: Détails orange
RECT 40 35 60 40 7

# ÉTAPE 9: Reflets blancs
RECT 42 31 43 34 1
RECT 57 31 58 34 1"""
    
    return solution

def solve_M_Chat_final_sans_commentaires(dataset_txt):
    """Version automatisée : analyse la grille et génère les rectangles optimaux pour couvrir exactement chaque couleur avec un algorithme glouton."""
    import json

    # Charger la grille depuis le dataset
    dataset = json.loads(dataset_txt)
    grid = dataset['grid']
    height = len(grid)
    width = len(grid[0])

    # Fonction pour trouver le plus grand rectangle possible dans les pixels restants
    def find_largest_rectangle(remaining):
        if not remaining:
            return None
        # Trouver le pixel le plus en haut à gauche
        min_y = min(y for y, x in remaining)
        min_x = min(x for y, x in remaining if y == min_y)
        # Étendre à droite
        x = min_x
        while x < width and (min_y, x) in remaining:
            x += 1
        max_x = x - 1
        # Étendre en bas
        y = min_y
        while y < height and all((y, xx) in remaining for xx in range(min_x, max_x + 1)):
            y += 1
        max_y = y - 1
        return min_x, min_y, max_x, max_y

    # Générer les actions : commencer par le fond (couleur 6), puis les autres couleurs
    actions = []
    for color in range(8):
        # Collecter les pixels à couvrir pour cette couleur
        remaining = set((y, x) for y in range(height) for x in range(width) if grid[y][x] == color)
        while remaining:
            rect = find_largest_rectangle(remaining)
            if rect:
                x1, y1, x2, y2 = rect
                actions.append(f"RECT {x1} {y1} {x2} {y2} {color}")
                # Retirer les pixels couverts
                for yy in range(y1, y2 + 1):
                    for xx in range(x1, x2 + 1):
                        remaining.discard((yy, xx))
            else:
                break  # Ne devrait pas arriver

    # Retourner la solution sous forme de chaîne
    return "\n".join(actions)

# FONCTIONS DU VIEWER
def apply_action(grid, action, target):
    """Applique une action RECT ou JOKER sur la grille."""
    parts = action.split()
    if parts[0] == "RECT":
        _, x1, y1, x2, y2, color = parts
        x1, y1, x2, y2, color = map(int, (x1, y1, x2, y2, color))
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                if 0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]:
                    grid[y, x] = color
    elif parts[0] == "JOKER":
        _, x1, y1, x2, y2 = parts
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                if 0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]:
                    grid[y, x] = target[y, x]
    return grid

def compute_score(target, current, step, max_actions):
    """Calcule le score à une étape donnée."""
    total_pixels = target.size
    correct_pixels = np.sum(target == current)
    
    if correct_pixels < total_pixels:
        return round(1_000_000 * correct_pixels / total_pixels)
    else:
        return round(1_000_000 * max_actions / step)

def viewer(input_file, solution_file):
    """Affiche la solution étape par étape"""
    # Charger dataset
    with open(input_file, "r", encoding='utf-8') as f:
        data = json.load(f)
    target = np.array(data["grid"])
    max_actions = data["maxActions"]

    # Charger solution
    with open(solution_file, "r", encoding='utf-8') as f:
        actions = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # Préparer états successifs
    states = [np.zeros_like(target)]
    for action in actions:
        new_state = states[-1].copy()
        new_state = apply_action(new_state, action, target)
        states.append(new_state)

    # Création figure
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    plt.subplots_adjust(bottom=0.2)

    # Palette de couleurs
    pixel_colormap = matplotlib.colors.ListedColormap([
        '#000000', '#FFFFFF', '#1E93FF', '#F93C31', 
        '#4FCC30', '#FFDC00', '#E53AA3', '#FF851B'
    ])

    # Images initiales
    im_target = axes[0].imshow(target, cmap=pixel_colormap, vmin=0, vmax=7)
    axes[0].set_title("Fresque cible")

    im_solution = axes[1].imshow(states[0], cmap=pixel_colormap, vmin=0, vmax=7)
    axes[1].set_title("Solution - étape 0")

    for ax in axes:
        ax.axis("on")
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(2)
        ax.set_xticks([])
        ax.set_yticks([])

    # Titre global
    title = fig.suptitle(f"Score étape 0 : {compute_score(target, states[0], 1, max_actions)}", fontsize=14)

    # Slider
    ax_slider = plt.axes([0.15, 0.05, 0.7, 0.05])
    slider = Slider(ax_slider, "Étape", 0, len(actions), valinit=0, valstep=1)

    def update(val):
        step = int(slider.val)
        im_solution.set_data(states[step])
        axes[1].set_title(f"Solution - étape {step}")
        score = compute_score(target, states[step], max(1, step), max_actions)
        title.set_text(f"Score étape {step} : {score}")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

# PROGRAMME PRINCIPAL
if __name__ == '__main__':
    dataset_name = "3_mchat"
    dataset_path = f'datasets/{dataset_name}.json'
    
    if not os.path.exists(dataset_path):
        print(f"❌ Fichier {dataset_path} non trouvé")
        exit()
    
    print(f"✅ Fichier trouvé: {dataset_path}")
    
    # Charge le dataset
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = f.read()
    
    print('---------------------------------')
    print(f'Solving {dataset_name}')
    
    # Teste la solution optimisée
    print("🎯 Test version optimisée (décomposition géométrique)")
    solution = solve_M_Chat_final_sans_commentaires(dataset)
    
    # Teste la solution
    score, is_valid, message = test_solution.get_solution_score(solution, dataset)
    
    if is_valid:
        print('✅ Solution valide!')
        print(f'Score: {score:_}')
        print(f'Message: {message}')
        
        # Sauvegarde AUTOMATIQUE
        solution_file = f'solutions/{dataset_name}_optimal.txt'
        with open(solution_file, 'w', encoding='utf-8') as f:
            f.write(solution)
        print(f'💾 Solution sauvegardée: {solution_file}')
        
        # LANCE LE VIEWER AUTOMATIQUEMENT
        print('🎨 Lancement du viewer...')
        try:
            viewer(dataset_path, solution_file)
        except Exception as e:
            print(f"❌ Erreur viewer: {e}")
        
    else:
        print('❌ Solution invalide')
        print(f'Message: {message}')