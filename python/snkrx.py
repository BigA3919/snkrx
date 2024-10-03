import csv
HEROS = {}
CLASSES = {}

with open('snkrx_data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        row_data = row[0].split(',')
        classes = [x for x in row_data[2:5] if x]
        if classes[0] == "Class": continue
        HEROS[row_data[0]] = classes
        for i in classes:
            if i == "explorer": continue
            if i in CLASSES:
                CLASSES.get(i).append(row_data[0])
            else:
                CLASSES[i] = [row_data[0]]
        
def find_all_of_class(key:str) -> list[str]:
    return CLASSES.get(key)
def get_optimal_build(type: str, size:int):
    build_list = [i for i in CLASSES.get(type)]
    max_score = -23
    new_guy = ""
    for hero in HEROS:
        if hero in build_list: continue
        score = get_points_from_move(build_list, hero)
        max_score = max(max_score, score)
        if max_score == score: new_guy = hero
    return new_guy
def get_points_from_move(hero_list: list[str], new_guy: str) -> int:
    points:int = 0
    class_list = HEROS.get(new_guy)
    for c in class_list:
        previous_sum = 0
        if c == "explorer": continue
        previous_sum = sum([previous_sum+1 for hero in hero_list if c in HEROS.get(hero)])
        if len(CLASSES.get(c)) < 7 and c != "archer":
            match previous_sum:
                case 0:
                    points += 2
                case 1:
                    points += 3
                case 2:
                    points += 2
                case 3:
                    points += 4
        elif c != "sorcerer":
            match previous_sum:
                case 0:
                    points += 1
                case 1:
                    points += 2
                case 2:
                    points += 4
                case 3:
                    points += 1
                case 4:
                    points += 2
                case 5:
                    points += 5
        else:
            match previous_sum:
                case 0:
                    points += 2
                case 1:
                    points += 3
                case 2:
                    points += 2
                case 3:
                    points += 3
                case 4:
                    points += 2
                case 5:
                    points += 4
    return points


print(find_all_of_class("ranger"))
print(get_optimal_build("swarmer", 7))