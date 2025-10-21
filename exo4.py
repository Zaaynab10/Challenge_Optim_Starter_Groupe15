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

    actions = []
    jokers_used = 0

    # Affichage des palets oranges (sans les pac-gommes et clyde)
    # co = 0
    # for ligne in target_grid :
    #     ro = 0
    #     for column in ligne :
    #         if target_grid[co][ro] == 7 :
    #             if target_grid[co][(ro + 1)] == 7 and target_grid[(co + 1)][ro] == 7 and target_grid[(co + 1)][(ro + 1)] == 7 :
    #                 action = f'RECT {ro} {co} {ro + 1} {co + 1} {7}'
    #                 actions.append(action)
    #         ro += 1
    #     co += 1

    # Affichage du niveau bleu
    coor = []
    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 2 :
                if ro != grid_width-1 and target_grid[co][(ro + 1)] == 2 :
                    if [co, ro + 1] not in coor :
                        aug = 1
                        num = 0
                        while ro + num != grid_width-1 and target_grid[co][(ro + aug)] == 2 :
                            aug += 1
                            num += 1
                            coor.append([co, ro + num])
                        action = f'RECT {ro} {co} {ro + num} {co} {2}'
                        actions.append(action)
                elif target_grid[(co + 1)][ro] == 2 :
                    if [co + 1, ro] not in coor :
                        aug = 1
                        num = 0
                        while target_grid[co + aug][(ro)] == 2 :
                            aug += 1
                            num += 1
                            coor.append([co + num, ro])
                        action = f'RECT {ro} {co} {ro} {co + num} {2}'
                        actions.append(action)
                # else :
                    # action = f'RECT {ro} {co} {ro} {co} {2}'
                    # actions.append(action)
            ro += 1
        co += 1


    # current_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
 
    # # Exemple de solution: on cherche itérativement des actions qui améliorent le score (stratégie Monte Carlo)
    # while len(actions) < max_actions:
    #     best_action = None
    #     best_score_increase = 0
    #     best_new_grid = None

    #     for _ in range(100):  # Nombre d'actions aléatoires à tester
    #         action_type = 'RECT' if jokers_used >= max_jokers else random.choice(['RECT', 'JOKER'])
    #         x1 = random.randint(0, grid_width - 1)
    #         y1 = random.randint(0, grid_height - 1)
    #         x2 = random.randint(x1, min(x1 + 10, grid_width - 1))
    #         y2 = random.randint(y1, min(y1 + 10, grid_height - 1))

    #         if action_type == 'RECT':
    #             color = random.randint(0, 7)
    #             action = f'RECT {x1} {y1} {x2} {y2} {color}'
    #         else:
    #             if (x2 - x1 + 1) * (y2 - y1 + 1) > max_joker_size:
    #                 continue  # Skip if the joker size exceeds the maximum allowed
    #             action = f'JOKER {x1} {y1} {x2} {y2}'

        #     # Simuler l'action et calculer l'augmentation du score
        #     simulated_grid = [row[:] for row in current_grid]
        #     if action.startswith('RECT '):
        #         _, sx1, sy1, sx2, sy2, scolor = action.split()
        #         sx1, sy1, sx2, sy2, scolor = map(int, (sx1, sy1, sx2, sy2, scolor))
        #         for y in range(sy1, sy2 + 1):
        #             for x in range(sx1, sx2 + 1):
        #                 simulated_grid[y][x] = scolor
        #     elif action.startswith('JOKER '):
        #         _, sx1, sy1, sx2, sy2 = action.split()
        #         sx1, sy1, sx2, sy2 = map(int, (sx1, sy1, sx2, sy2))
        #         for y in range(sy1, sy2 + 1):
        #             for x in range(sx1, sx2 + 1):
        #                 simulated_grid[y][x] = target_grid[y][x]

        #     current_score = sum(1 for y in range(grid_height) for x in range(grid_width) if simulated_grid[y][x] == target_grid[y][x])
        #     score_increase = current_score - sum(1 for y in range(grid_height) for x in range(grid_width) if current_grid[y][x] == target_grid[y][x])

        #     if score_increase > best_score_increase:
        #         best_score_increase = score_increase
        #         best_action = action
        #         best_new_grid = simulated_grid

        # if best_action:
        #     actions.append(best_action)
        #     current_grid = best_new_grid
        #     if best_action.startswith('JOKER '):
        #         jokers_used += 1
        # else:
        #     break

    return "\n".join(actions)


if __name__ == '__main__':
    dataset_file = "4_pacman"
    dataset = open(f'datasets/{dataset_file}.json').read()

    print('---------------------------------')
    print(f'Solving {dataset_file}')
    solution = solve(dataset)
    print('---------------------------------')
    score, is_valid, message = test_solution.get_solution_score(solution, dataset)

    if is_valid:
        print('✅ Solution is valid!')
        print(f'Message: {message}')
        print(f'Score: {score:_}')
        
        save = input('Save solution? (y/n): ')
        if save.lower() == 'y':
            date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'solutions/{dataset_file}_{score}_{date}.txt'

            with open(file_name, 'w') as f:
                f.write(solution)
            print('Solution saved')
        else:
            print('Solution not saved')
        
    else:
        print('❌ Solution is invalid')
        print(f'Message: {message}')

        save = input('Save solution? (y/n): ')
        if save.lower() == 'y':
            date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'solutions/{dataset_file}_{score}_{date}.txt'

            with open(file_name, 'w') as f:
                f.write(solution)
            print('Solution saved')
        else:
            print('Solution not saved')