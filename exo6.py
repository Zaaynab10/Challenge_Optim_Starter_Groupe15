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

    coorNoir = []
    coorBlanc = []
    coorRouge = []
    coorVert = []
    coorJaune = []
    coorRose = []
    coorOrange = []

    action = f'RECT 0 0 999 999 2'
    actions.append(action)

    while jokers_used != 200 :
        co = 0
        while co + 9 != grid_height - 1 and jokers_used != 200 :
            ro = 0
            while ro + 9 != grid_height - 1 and jokers_used != 200 :
                action = f'JOKER {ro} {co} {ro + 9} {co + 9}'
                actions.append(action)
                jokers_used += 1
                testCo = 133
                while testCo <= 142 :
                    testRo = 92
                    while testRo <= 131 :
                        if target_grid[testCo][testRo] == 0:
                            coorNoir.append([testCo, testRo])
                        elif target_grid[testCo][testRo] == 1:
                            coorBlanc.append([testCo, testRo])
                        elif target_grid[testCo][testRo] == 3:
                            coorRouge.append([testCo, testRo])
                        elif target_grid[testCo][testRo] == 4:
                            coorVert.append([testCo, testRo])
                        elif target_grid[testCo][testRo] == 5:
                            coorJaune.append([testCo, testRo])
                        elif target_grid[testCo][testRo] == 6:
                            coorRose.append([testCo, testRo])
                        elif target_grid[testCo][testRo] == 7:
                            coorOrange.append([testCo, testRo])
                        testRo += 1
                    testCo += 1
                ro += 10
            co += 10

    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 4 and len(actions) != 2000:
                if [co, ro] not in coorVert :
                    maxX = 0
                    num = 0
                    while ro + num != grid_width and target_grid[co][(ro + num)] not in [2]  :
                        num += 1
                    if num == 0 :
                        maxX = ro + num
                    else :
                        maxX = ro + num - 1
                    
                    maxY = 0
                    num = 0
                    while co + num != grid_height and target_grid[co + num][(ro)] not in [2] :
                        num += 1
                    if num == 0 :
                        maxY = co + num
                    else :
                        maxY = co + num - 1
                    
                    coorTemp = []
                    testCo = co
                    while testCo <= maxY :
                        testRo = ro
                        while testRo <= maxX :
                            coorTemp.append([testCo, testRo])
                            testRo += 1
                        testCo += 1

                    key = 0
                    for elem in coorTemp :
                        if target_grid[elem[0]][elem[1]] in [2] :
                            if elem[0] != coorTemp[0][0] :
                                keyDeux=0
                                for elemDeux in coorTemp :
                                    if elemDeux == [coorTemp[key][0] - 1, maxX] :
                                        key = keyDeux
                                        break
                                    keyDeux += 1
                                action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {4}'
                                actions.append(action)
                                break
                            else :
                                action = f'RECT {ro} {co} {coorTemp[key - 1][1]} {coorTemp[key - 1][0]} {4}'
                                actions.append(action)
                                key -= 1
                                break
                        elif coorTemp[len(coorTemp) - 1] == elem :
                            action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {4}'
                            actions.append(action)
                            break
                        key += 1

                    keyLog = 0
                    while keyLog <= key :
                        if coorTemp[keyLog] not in coorVert and target_grid[coorTemp[keyLog][0]][coorTemp[keyLog][1]] == 4 :
                            coorVert.append(coorTemp[keyLog])
                        keyLog += 1
                    
            ro += 1
        co += 1

    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 1 and len(actions) != 2000:
                if [co, ro] not in coorBlanc :
                    maxX = 0
                    num = 0
                    while ro + num != grid_width and target_grid[co][(ro + num)] not in [2, 4]  :
                        num += 1
                    if num == 0 :
                        maxX = ro + num
                    else :
                        maxX = ro + num - 1
                    
                    maxY = 0
                    num = 0
                    while co + num != grid_height and target_grid[co + num][(ro)] not in [2, 4] :
                        num += 1
                    if num == 0 :
                        maxY = co + num
                    else :
                        maxY = co + num - 1
                    
                    coorTemp = []
                    testCo = co
                    while testCo <= maxY :
                        testRo = ro
                        while testRo <= maxX :
                            coorTemp.append([testCo, testRo])
                            testRo += 1
                        testCo += 1

                    key = 0
                    for elem in coorTemp :
                        if target_grid[elem[0]][elem[1]] in [2, 4] :
                            if elem[0] != coorTemp[0][0] :
                                keyDeux=0
                                for elemDeux in coorTemp :
                                    if elemDeux == [coorTemp[key][0] - 1, maxX] :
                                        key = keyDeux
                                        break
                                    keyDeux += 1
                                action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {1}'
                                actions.append(action)
                                break
                            else :
                                action = f'RECT {ro} {co} {coorTemp[key - 1][1]} {coorTemp[key - 1][0]} {1}'
                                actions.append(action)
                                key -= 1
                                break
                        elif coorTemp[len(coorTemp) - 1] == elem :
                            action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {1}'
                            actions.append(action)
                            break
                        key += 1

                    keyLog = 0
                    while keyLog <= key :
                        if coorTemp[keyLog] not in coorBlanc and target_grid[coorTemp[keyLog][0]][coorTemp[keyLog][1]] == 1 :
                            coorBlanc.append(coorTemp[keyLog])
                        keyLog += 1
                    
            ro += 1
        co += 1

    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 3 and len(actions) != 2000:
                if [co, ro] not in coorRouge :
                    maxX = 0
                    num = 0
                    while ro + num != grid_width and target_grid[co][(ro + num)] not in [1, 2, 4]  :
                        num += 1
                    if num == 0 :
                        maxX = ro + num
                    else :
                        maxX = ro + num - 1
                    
                    maxY = 0
                    num = 0
                    while co + num != grid_height and target_grid[co + num][(ro)] not in [1, 2, 4] :
                        num += 1
                    if num == 0 :
                        maxY = co + num
                    else :
                        maxY = co + num - 1
                    
                    coorTemp = []
                    testCo = co
                    while testCo <= maxY :
                        testRo = ro
                        while testRo <= maxX :
                            coorTemp.append([testCo, testRo])
                            testRo += 1
                        testCo += 1

                    key = 0
                    for elem in coorTemp :
                        if target_grid[elem[0]][elem[1]] in [1, 2, 4] :
                            if elem[0] != coorTemp[0][0] :
                                keyDeux=0
                                for elemDeux in coorTemp :
                                    if elemDeux == [coorTemp[key][0] - 1, maxX] :
                                        key = keyDeux
                                        break
                                    keyDeux += 1
                                action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {3}'
                                actions.append(action)
                                break
                            else :
                                action = f'RECT {ro} {co} {coorTemp[key - 1][1]} {coorTemp[key - 1][0]} {3}'
                                actions.append(action)
                                key -= 1
                                break
                        elif coorTemp[len(coorTemp) - 1] == elem :
                            action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {3}'
                            actions.append(action)
                            break
                        key += 1

                    keyLog = 0
                    while keyLog <= key :
                        if coorTemp[keyLog] not in coorRouge and target_grid[coorTemp[keyLog][0]][coorTemp[keyLog][1]] == 3 :
                            coorRouge.append(coorTemp[keyLog])
                        keyLog += 1
                    
            ro += 1
        co += 1

    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 0 and len(actions) != 2000:
                if [co, ro] not in coorNoir :
                    maxX = 0
                    num = 0
                    while ro + num != grid_width and target_grid[co][(ro + num)] not in [1, 2, 3, 4]  :
                        num += 1
                    if num == 0 :
                        maxX = ro + num
                    else :
                        maxX = ro + num - 1
                    
                    maxY = 0
                    num = 0
                    while co + num != grid_height and target_grid[co + num][(ro)] not in [1, 2, 3, 4] :
                        num += 1
                    if num == 0 :
                        maxY = co + num
                    else :
                        maxY = co + num - 1
                    
                    coorTemp = []
                    testCo = co
                    while testCo <= maxY :
                        testRo = ro
                        while testRo <= maxX :
                            coorTemp.append([testCo, testRo])
                            testRo += 1
                        testCo += 1

                    key = 0
                    for elem in coorTemp :
                        if target_grid[elem[0]][elem[1]] in [1, 2, 3, 4] :
                            if elem[0] != coorTemp[0][0] :
                                keyDeux=0
                                for elemDeux in coorTemp :
                                    if elemDeux == [coorTemp[key][0] - 1, maxX] :
                                        key = keyDeux
                                        break
                                    keyDeux += 1
                                action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {0}'
                                actions.append(action)
                                break
                            else :
                                action = f'RECT {ro} {co} {coorTemp[key - 1][1]} {coorTemp[key - 1][0]} {0}'
                                actions.append(action)
                                key -= 1
                                break
                        elif coorTemp[len(coorTemp) - 1] == elem :
                            action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {0}'
                            actions.append(action)
                            break
                        key += 1

                    keyLog = 0
                    while keyLog <= key :
                        if coorTemp[keyLog] not in coorNoir and target_grid[coorTemp[keyLog][0]][coorTemp[keyLog][1]] == 0 :
                            coorNoir.append(coorTemp[keyLog])
                        keyLog += 1
                    
            ro += 1
        co += 1
    
    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 6 and len(actions) != 2000:
                if [co, ro] not in coorRose :
                    maxX = 0
                    num = 0
                    while ro + num != grid_width and target_grid[co][(ro + num)] not in [0, 1, 2, 3, 4]  :
                        num += 1
                    if num == 0 :
                        maxX = ro + num
                    else :
                        maxX = ro + num - 1
                    
                    maxY = 0
                    num = 0
                    while co + num != grid_height and target_grid[co + num][(ro)] not in [0, 1, 2, 3, 4] :
                        num += 1
                    if num == 0 :
                        maxY = co + num
                    else :
                        maxY = co + num - 1
                    
                    coorTemp = []
                    testCo = co
                    while testCo <= maxY :
                        testRo = ro
                        while testRo <= maxX :
                            coorTemp.append([testCo, testRo])
                            testRo += 1
                        testCo += 1

                    key = 0
                    for elem in coorTemp :
                        if target_grid[elem[0]][elem[1]] in [0, 1, 2, 3, 4] :
                            if elem[0] != coorTemp[0][0] :
                                keyDeux=0
                                for elemDeux in coorTemp :
                                    if elemDeux == [coorTemp[key][0] - 1, maxX] :
                                        key = keyDeux
                                        break
                                    keyDeux += 1
                                action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {6}'
                                actions.append(action)
                                break
                            else :
                                action = f'RECT {ro} {co} {coorTemp[key - 1][1]} {coorTemp[key - 1][0]} {6}'
                                actions.append(action)
                                key -= 1
                                break
                        elif coorTemp[len(coorTemp) - 1] == elem :
                            action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {6}'
                            actions.append(action)
                            break
                        key += 1

                    keyLog = 0
                    while keyLog <= key :
                        if coorTemp[keyLog] not in coorRose and target_grid[coorTemp[keyLog][0]][coorTemp[keyLog][1]] == 6 :
                            coorRose.append(coorTemp[keyLog])
                        keyLog += 1
                    
            ro += 1
        co += 1

        co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 5 and len(actions) != 2000:
                if [co, ro] not in coorJaune :
                    maxX = 0
                    num = 0
                    while ro + num != grid_width and target_grid[co][(ro + num)] not in [0, 1, 2, 3, 4, 6]  :
                        num += 1
                    if num == 0 :
                        maxX = ro + num
                    else :
                        maxX = ro + num - 1
                    
                    maxY = 0
                    num = 0
                    while co + num != grid_height and target_grid[co + num][(ro)] not in [0, 1, 2, 3, 4, 6] :
                        num += 1
                    if num == 0 :
                        maxY = co + num
                    else :
                        maxY = co + num - 1
                    
                    coorTemp = []
                    testCo = co
                    while testCo <= maxY :
                        testRo = ro
                        while testRo <= maxX :
                            coorTemp.append([testCo, testRo])
                            testRo += 1
                        testCo += 1

                    key = 0
                    for elem in coorTemp :
                        if target_grid[elem[0]][elem[1]] in [0, 1, 2, 3, 4, 6] :
                            if elem[0] != coorTemp[0][0] :
                                keyDeux=0
                                for elemDeux in coorTemp :
                                    if elemDeux == [coorTemp[key][0] - 1, maxX] :
                                        key = keyDeux
                                        break
                                    keyDeux += 1
                                action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {5}'
                                actions.append(action)
                                break
                            else :
                                action = f'RECT {ro} {co} {coorTemp[key - 1][1]} {coorTemp[key - 1][0]} {5}'
                                actions.append(action)
                                key -= 1
                                break
                        elif coorTemp[len(coorTemp) - 1] == elem :
                            action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {5}'
                            actions.append(action)
                            break
                        key += 1

                    keyLog = 0
                    while keyLog <= key :
                        if coorTemp[keyLog] not in coorJaune and target_grid[coorTemp[keyLog][0]][coorTemp[keyLog][1]] == 5 :
                            coorJaune.append(coorTemp[keyLog])
                        keyLog += 1
                    
            ro += 1
        co += 1

    co = 0
    for ligne in target_grid :
        ro = 0
        for _ in ligne :
            if target_grid[co][ro] == 7 and len(actions) != 2000:
                if [co, ro] not in coorOrange :
                    maxX = 0
                    num = 0
                    while ro + num != grid_width and target_grid[co][(ro + num)] not in [0, 1, 2, 3, 4, 5, 6] :
                        num += 1
                    if num == 0 :
                        maxX = ro + num
                    else :
                        maxX = ro + num - 1
                    
                    maxY = 0
                    num = 0
                    while co + num != grid_height and target_grid[co + num][(ro)] not in [0, 1, 2, 3, 4, 5, 6] :
                        num += 1
                    if num == 0 :
                        maxY = co + num
                    else :
                        maxY = co + num - 1
                    
                    coorTemp = []
                    testCo = co
                    while testCo <= maxY :
                        testRo = ro
                        while testRo <= maxX :
                            coorTemp.append([testCo, testRo])
                            testRo += 1
                        testCo += 1

                    key = 0
                    for elem in coorTemp :
                        if target_grid[elem[0]][elem[1]] in [0, 1, 2, 3, 4, 5, 6] :
                            if elem[0] != coorTemp[0][0] :
                                keyDeux=0
                                for elemDeux in coorTemp :
                                    if elemDeux == [coorTemp[key][0] - 1, maxX] :
                                        key = keyDeux
                                        break
                                    keyDeux += 1
                                action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {7}'
                                actions.append(action)
                                break
                            else :
                                action = f'RECT {ro} {co} {coorTemp[key - 1][1]} {coorTemp[key - 1][0]} {7}'
                                actions.append(action)
                                key -= 1
                                break
                        elif coorTemp[len(coorTemp) - 1] == elem :
                            action = f'RECT {ro} {co} {coorTemp[key][1]} {coorTemp[key][0]} {7}'
                            actions.append(action)
                            break
                        key += 1

                    keyLog = 0
                    while keyLog <= key :
                        if coorTemp[keyLog] not in coorOrange and target_grid[coorTemp[keyLog][0]][coorTemp[keyLog][1]] == 7 :
                            coorOrange.append(coorTemp[keyLog])
                        keyLog += 1
                    
            ro += 1
        co += 1

    return "\n".join(actions)


if __name__ == '__main__':
    dataset_file = "6_wplace"
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