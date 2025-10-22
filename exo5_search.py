import json
import random
import test_solution
import datetime


def solve(dataset_txt):
    # Lecture du dataset
    dataset = json.loads(dataset_txt)

    target_grid = dataset['grid']
    max_actions = dataset['maxActions']
    max_jokers = dataset['maxJokers']
    max_joker_size = dataset['maxJokerSize']
    grid_height = len(target_grid)
    grid_width = len(target_grid[0])

    soluceText = open("solutions/5_banksy_best_incomplete.txt").read()
    soluceTab = soluceText.splitlines()
    soluce = []
    for elem in soluceTab :
        soluce.append(elem.split())

    display = []
    val = 0
    while val < grid_height :
        display.append([])
        val += 1

    for elem in display :
        val = 0
        while val < grid_height :
            elem.append(0)
            val += 1

    for step in soluce :
        if step[0] == "RECT":

            valX = int(step[1])
            while valX != int(step[3]) + 1 :
                valY = int(step[2])
                while valY != int(step[4]) + 1 :
                    display[valY][valX] = int(step[5])
                    valY += 1
                valX += 1

        elif step[0] == "JOKER":
            valX = int(step[1])
            while valX != int(step[3]) + 1 :
                valY = int(step[2])
                while valY != int(step[4]) + 1 :
                    display[valY][valX] = target_grid[valY][valX]
                    valY += 1
                valX += 1
    
    diff = 0
    valUne = 0
    for elem in target_grid :
        valDeux = 0
        for e in elem :
            if e != display[valUne][valDeux] :
                print(valDeux)
                print(valUne)
                print(target_grid[valUne][valDeux])
                diff += 1
            valDeux += 1
        valUne += 1
    # print(diff)










if __name__ == '__main__':
    dataset_file = "5_banksy"
    dataset = open(f'datasets/{dataset_file}.json').read()

    print('---------------------------------')
    print(f'Solving {dataset_file}')
    solution = solve(dataset)