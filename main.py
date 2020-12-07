from datetime import date


class Any():
    def __eq__(self, other):
        return True

any = Any()


def day1():
    with open(r'input/day1.txt') as f:
        numbers = sorted(int(x) for x in f.readlines())
    for i, num1 in enumerate(numbers):
        for j, num2 in enumerate(numbers[i + 1:]):
            if (num1 + num2) == 2020:
                part_1 = num1 * num2
            for num3 in numbers[i + j:]:
                if (num1 + num2 + num3) == 2020:
                    part_2 = num1 * num2 * num3
                    break
    return part_1, part_2


def day2():
    with open('input/day2.txt') as f:
        passwords = f.readlines()
    part_1 = 0
    part_2 = 0
    for password in passwords:
        constraint, letter, password = password.split()
        val1, val2 = constraint.split('-')
        letter = letter[0]
        if int(val1) <= password.count(letter) <= int(val2):
            part_1 += 1
        if (password[int(val1) - 1] == letter) ^ (password[int(val2) - 1] ==
                                                  letter):
            part_2 += 1
    return part_1, part_2


def day3():
    with open('input/day3.txt') as f:
        input_data = [list(line.strip()) for line in f.readlines()]
    product = 1
    answers = {}
    for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        answer, x, y = 0, 0, 0
        while True:
            x = (x + dx) % len(input_data[0])
            y += dy
            try:
                answer += (input_data[y][x] == '#')

            except IndexError:
                answers[(dx, dy)] = answer
                product *= answer
                break
    part_1 = answers[(3, 1)]
    return part_1, product


def day4(input_values):
    def isvalid(field):
        k, v = field.split(':')
        valid = {'byr': lambda x: 1920 <= int(x) <= 2002,
                 'iyr': lambda x: 2010 <= int(x) <= 2020,
                 'eyr': lambda x: 2020 <= int(x) <= 2030,
                 'hgt': lambda x: (x[-2:] in ('cm', 'in')) and valid[x[-2:]](x[:-2]),
                 'cm': lambda x: 150 <= int(x) <= 193,
                 'in': lambda x: 59 <= int(x) <= 76,
                 'hcl': lambda x: (x[0] == '#' and len(x) == 7 and all(c in 'abcdef0123456789' for c in x[1:])),
                 'ecl': lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
                 'pid': lambda x: len(x) == 9 and bool(int(x)),
                 'cid': lambda x: True,
                 }
        return valid[k](v)

    part_1, part_2 = 0, 0

    with open(r"input/day4.txt") as f:
        _input = [x.strip() for x in f.read().split('\n\n')]
    passports = []
    required = {'hcl', 'hgt', 'ecl', 'byr', 'iyr', 'eyr', 'pid'}

    for line in _input:
        fields = line.split()
        passport = {field.split(':')[0] for field in fields}
        valid_passport = {field.split(':')[0] for field in fields if isvalid(field)}
        if not (required - passport):
            part_1 += 1
        if not (required - valid_passport):
            part_2 += 1
    return part_1, part_2


def day5(input_values: list) -> tuple:
    """
    Build a list of binary numbers, sorted lexigraphically, e.g. for left-right:
    ['000', '001', '010', '011', '100', '101', '110', '111']
    Translate to LR (or FB)
    build a dictionary mapping translated string to index {'LLL' : 0, ...}
    calculate answer
    """
    part_1 = 0
    part_2 = None
    lr_list = sorted(bin(x)[2:].zfill(3) for x in range(8))
    lr_trans = str.maketrans('01', 'LR')
    lr_dict = {s.translate(lr_trans): i for i, s in enumerate(lr_list)}
    fb_list = sorted(bin(x)[2:].zfill(7) for x in range(128))
    fb_trans = str.maketrans('01', 'FB')
    fb_dict = {s.translate(fb_trans): i for i, s in enumerate(fb_list)}
    seat_ids = []

    for boarding_pass in input_values:
        row = fb_dict[boarding_pass.strip()[:7]]
        column = lr_dict[boarding_pass.strip()[7:]]
        seat_id = (8 * row) + column
        seat_ids.append(seat_id)
        part_1 = max(part_1, seat_id)
    seat_ids.sort()
    part_2 = seat_ids[0]
    for seat_id in seat_ids:
        if seat_id > (part_2):
            part_2 = seat_id - 1
            break
        else:
            part_2 += 1

    return part_1, part_2


day5_test_values = {"FBFBBFFRLR": (357, any),
                    "BFFFBBFRRR": (567, any),
                    "FFFBBBFRRR": (119, any),
                    "BBFFBBFRLL": (820, any),
                    }


def day6(input_values: str) -> tuple:
    """template"""
    part_1 = 0
    part_2 = 0
    groups = input_values.split('\n\n')

    for group in groups:
        person_yesses = [set(person.strip()) for person in group.split('\n')]
        all_yesses = person_yesses.pop().intersection(*person_yesses)
        part_2 += len(all_yesses)
        group_yesses = set(group.replace('\n', ''))
        part_1 += len(group_yesses)

    return part_1, part_2


day6_test_values = {"abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb": (11, 6),
                    }


def day7(input_values: str) -> tuple:
    """Build a graph of bags, find the set of unique parents, recursively find children"""
    def number_of_children(bag) -> int:
        """recursively find the number of child bags"""
        nonlocal bags
        children = 0
        for child_bag, number in bags[bag].items():
            children += number * (number_of_children(child_bag) +1)
        return children
    part_1 = None
    part_2 = None
    lines = input_values.replace('bags', 'bag').split('\n')
    bags = {}
    for line in lines:
        container, contents = line.strip('.').split(' contain ')
        if contents == 'no other bag':
            bags[container] = {}
            continue
        contents = {bag[2:] : int(bag[0]) for bag in contents.split(', ')}
        bags[container] = contents
    print(bags)
    can_contain = ['shiny gold bag',]
    for target in can_contain:
        for bag in bags.keys():
            if target in bags[bag].keys():
                can_contain.append(bag)

    print(can_contain)
    part_1 = len(set(can_contain)) -1
    part_2 = number_of_children('shiny gold bag')
    return part_1, part_2


day7_test_values = {"""light red bags contain 1 bright white bag, 2 muted yellow bags.\ndark orange bags contain 3 bright white bags, 4 muted yellow bags.\nbright white bags contain 1 shiny gold bag.\nmuted yellow bags contain 2 shiny gold bags, 9 faded blue bags.\nshiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.\ndark olive bags contain 3 faded blue bags, 4 dotted black bags.\nvibrant plum bags contain 5 faded blue bags, 6 dotted black bags.\nfaded blue bags contain no other bags.\ndotted black bags contain no other bags.""": (4, 32),
                    """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""" : (any, 126)
                    }


def dayx(input_values: str) -> tuple:
    """template"""
    part_1 = None
    part_2 = None
    ...

    return part_1, part_2


if __name__ == '__main__':
    today = date.today()
    if today.month == 12:
        print('Merry Christmas')
    for input_value, answer in day7_test_values.items():
        try:
            assert answer == day7(input_value)
        except Exception as e:
            print(input_value, answer, day7(input_value, ))
            raise e
    with open('input/day7.txt') as f:
        input_values = f.read()
    print(day7(input_values))
