from src.game import Game
import numpy as np
import random
import os

DATASETS_DIR = '../datasets/'
if not os.path.exists(DATASETS_DIR):
    raise FileNotFoundError(f"Le dossier des datasets '{DATASETS_DIR}' n'existe pas!")



def get_grid(dataset_file=None):
    import json
    if dataset_file is None:
        dataset_file = DATASETS_DIR + random.choice(os.listdir(DATASETS_DIR))
        print("Using random dataset file:", dataset_file)

    with open(dataset_file, "r") as f:
        data = json.load(f)
    return os.path.splitext(os.path.basename(dataset_file))[0], data

def generate_actions(grid_size: tuple, joker: bool= False) -> str:
    grid_height, grid_width = grid_size
    random_point_1 = (np.random.randint(0, grid_width), np.random.randint(0, grid_height))
    random_point_2 = (np.random.randint(random_point_1[0], grid_width), np.random.randint(random_point_1[1], grid_height))
    if joker:
        return "JOKER " + "{} {} {} {}".format(random_point_1[0], random_point_1[1], random_point_2[0], random_point_2[1])
    else:
        color = random.randint(0, 7)
        return "RECT " + "{} {} {} {} {}".format(random_point_1[0], random_point_1[1], random_point_2[0], random_point_2[1], color)


if __name__ == '__main__':
    file_name, file_content = get_grid()#"../datasets/3_mchat.json")
    grid = np.array(file_content["grid"])

    print("Grid shape:", np.array(grid).shape)
    print("Grid size:", np.array(grid).size)
    
    game = Game(np.array(grid), title=str.split(file_name, "_")[1])

    while True:
        next_action = generate_actions(np.array(grid).shape, joker=random.random() < 0.3)
        print("next action:", next_action)
        game.play_step(next_action)