import csv
HEROS = {str:list[str]}
CLASSES = {}
CLASS_TYPES = {
    "T1" : [],
    "T2" : [],
    "T3" : []
}
SYNERGIES = [
    ("warrior", "forcer"),
    ("archer", "rogue"),
    ("nuker", "mage"),
    ("infestor", "curser"),
    ("healer", "warrior")
    ("mercenary", "curser")
]
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
    for c in CLASSES:
        if len(CLASSES.get(c)) < 7 and c != "ranger" or c == "voider":
            CLASS_TYPES.get("T2").append(c)
        elif c == "sorcerer":
            CLASS_TYPES.get("T3").append(c)
        else:
            CLASS_TYPES.get("T1").append(c)

        
#returns all classes that have at least one hero in them in a given build
def get_all_classes(heros:list[str]) -> list[str]:
    class_list = []
    if len(heros) == 0: return []
    for h in heros:
        class_list += [x for x in HEROS.get(h) if x not in class_list]
    return class_list

#checks class type
def get_class_type(type:str) -> int:
    if type in CLASS_TYPES.get("T1"):
        return 1
    if type in CLASS_TYPES.get("T2"):
        return 2
    return 3

#checks whether a hero is a part of at least one class from a list of classes
def hero_contains_class(hero:str, class_list:list[str]) -> bool:
    return len(set(class_list).intersection(HEROS.get(hero))) != 0

#gets the optimal build by picking the highest scoring addition per turn
def get_optimal_build_v1(type: str, size:int) -> list[str]:
    build_list = []
    class_type = get_class_type(type)
    class_length = 4 if class_type == 2 else 6
    #while(len(build_list) < class_length):
    if(len(CLASSES.get(type)) == class_length and len(CLASSES.get(type)) < size):
        build_list += CLASSES.get(type)
    else:
        potential_list = CLASSES.get(type)
        while len(build_list) != class_length:
            max_score = -23
            new_guy = ""
            for hero in potential_list:
                if hero in build_list : continue
                score = get_points_from_move(build_list, hero)
                max_score = max(max_score, score)
                if max_score == score: new_guy = hero
            build_list.append(new_guy)
    while len(build_list) != size:
        max_score = -23
        new_guy = ""
        class_list = get_all_classes(build_list)
        for hero in HEROS:
            if hero in build_list : continue
            if not hero_contains_class(hero, class_list): continue
            score = get_points_from_move(build_list, hero)
            max_score = max(max_score, score)
            if max_score == score: new_guy = hero
        build_list.append(new_guy)
    return build_list

#scores a move
def get_points_from_move(hero_list: list[str], new_guy: str) -> int:
    points:int = 0
    class_list = HEROS.get(new_guy)
    for c in class_list:
        previous_sum = 0
        if c == "explorer": continue
        previous_sum = sum([previous_sum+1 for hero in hero_list if c in HEROS.get(hero)])
        if get_class_type(c) == 2:
            match previous_sum:
                case 0:
                    points += 0
                case 1:
                    points += 3
                case 2:
                    points += 1
                case 3:
                    points += 4
        elif c != "sorcerer":
            match previous_sum:
                case 0:
                    points += 0
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
                    points += 0
                case 1:
                    points += 3
                case 2:
                    points += 1
                case 3:
                    points += 3
                case 4:
                    points += 1
                case 5:
                    points += 4
    return points

#displays a build
def display_build(build:list[str]):
    classes = get_all_classes(build)
    for c in classes:
        heros_in_class = [h for h in CLASSES.get(c) if h in build]
        print(f"{c}: {heros_in_class} : {len(heros_in_class)} / {4 if get_class_type(c) == 2 else 6}")

#print(find_all_of_class("ranger"))
#display_build(CLASSES.get("swarmer"))
print("MAGES:")
display_build(get_optimal_build_v1("mage", 11))
print("NUKERS:")
display_build(get_optimal_build_v1("warrior", 11))
