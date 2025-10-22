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

    # Affichage du lanceur noir
    coor = []

    action = f'RECT {0} {0} {399} {399} {1}'
    actions.append(action)

    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 0 and len(actions) != 5000:
                if target_grid[co][(ro + 1)] == 0 or target_grid[(co + 1)][ro] == 0 :
                    # if [co, ro, 0] not in coor :
                    if [co, ro] not in coor :
                        maxX = []
                        aug = 1
                        num = 0
                        while target_grid[co][(ro + aug)] == 0 :
                            aug += 1
                            num += 1
                            # coor.append([co, ro + num])
                        maxX = [co, ro + num]
                        maxY = []
                        aug = 1
                        num = 0
                        while target_grid[co + aug][(ro)] == 0 :
                            aug += 1
                            num += 1
                            # coor.append([co + num, ro])
                        maxY = [co + num, ro]
                        aug = 1
                        num = 0

                        while maxY[1] + num <= maxX[1] and target_grid[maxY[0]][ro + aug] == 0 :
                            aug += 1
                            num += 1
                        action = f'RECT {ro} {co} {ro + num} {maxY[0]} {0}'
                        actions.append(action)
                        
                        roLog = ro
                        while roLog != ro + num + 1 :
                            coLog = co
                            while coLog != maxY[0] + 1 :
                                # coor.append([coLog, roLog, 0])
                                if [coLog, roLog] not in coor :
                                    coor.append([coLog, roLog])
                                coLog += 1
                            roLog += 1
                else :
                    if [co, ro] not in coor :
                        action = f'RECT {ro} {co} {ro} {co} {0}'
                        actions.append(action)
                        coor.append([co, ro])
            ro += 1
        co += 1


    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 1 and len(actions) != 5000:
                # if [co, ro, 0] in coor :
                if [co, ro] in coor :

                    maxX = []
                    aug = 1
                    num = 0
                    while target_grid[co][(ro + aug)] == 1 and [co, (ro + aug)] in coor :
                        aug += 1
                        num += 1
                    maxX = [co, ro + num]

                    maxY = []
                    aug = 1
                    num = 0
                    while target_grid[co + aug][(ro)] == 1 and [co + aug, (ro)] in coor :
                        aug += 1
                        num += 1
                    maxY = [co + num, ro]

                    aug = 1
                    num = 0
                    while maxY[1] + num <= maxX[1] and target_grid[maxY[0]][ro + aug] == 1 and [maxY[0], ro + num] in coor :
                        aug += 1
                        num += 1
                    action = f'RECT {ro} {co} {ro + num} {maxY[0]} {1}'
                    actions.append(action)
                        
                    roLog = ro
                    while roLog != ro + num + 1 :
                        coLog = co
                        while coLog != maxY[0] + 1 :
                            if [coLog, roLog] in coor :
                                coor.remove([coLog, roLog])
                                # coor.remove([coLog, roLog, 0])
                                # coor.append([coLog, roLog, 1])
                            coLog += 1
                        roLog += 1
            ro += 1
        co += 1

    
    # noir = 0
    # co = 0
    # for ligne in target_grid :
    #     ro = 0
    #     for _ in ligne :
    #         if target_grid[co][ro] == 0 :
    #             noir += 1
    #         ro += 1
    #     co += 1
    # print(noir)
    # print(len(coor))

    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] != 0 and target_grid[co][ro] != 1 and jokers_used != 100 and len(actions) != 5000 :
                if [co, ro] not in coor :
                    action = f"JOKER {ro} {co} {ro + 9} {co + 9}"
                    actions.append(action)
                    jokers_used += 1

                    roDel = ro
                    while roDel != ro + 9 :
                        coDel = co
                        while coDel != co + 9 :
                            coor.append([coDel, roDel])
                            # coor.append([coDel, roDel, "JOKER"])
                            coDel += 1
                        roDel += 1
            ro += 1
        co += 1

    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] != 1 and [co, ro] not in coor :
            # if [co, ro, target_grid[co][ro]] not in coor :
                action = f"RECT {ro} {co} {ro} {co} {target_grid[co][ro]}"
                actions.append(action)
            ro += 1
        co += 1

    return "\n".join(actions)


if __name__ == '__main__':
    dataset_file = "5_banksy"
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


#  and target_grid[co][(ro + aug)] in coor
#  and target_grid[co + aug][(ro)] in coor
#  and target_grid[maxY[0]][ro + num] in coor