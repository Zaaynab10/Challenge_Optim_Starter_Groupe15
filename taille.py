import json

# dataset_file = "1_example"
# dataset_file = "2_invader"
# dataset_file = "3_mchat"
dataset_file = "4_pacman"
# dataset_file = "5_banksy"
# dataset_file = "6_wplace"

dataset_js = open(f'datasets/{dataset_file}.json').read()

dataset = json.loads(dataset_js)

target_grid = dataset['grid']
grid_height = len(target_grid)
grid_width = len(target_grid[0])

grid_size = grid_width * grid_height

print(f"Taille : {grid_height}, Largeur : {grid_width}")
print(grid_height)
print("-----------")
print(grid_width)
print("-----------")
print(grid_size)