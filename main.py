from datetime import date

class Any():
    def __eq__(self, other):
        return True
    def __ne__(self, other):
        return False

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


def day5(input_values : list) -> tuple:
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
    lr_dict = {s.translate(lr_trans):i for i, s in enumerate(lr_list)}
    fb_list = sorted(bin(x)[2:].zfill(7) for x in range(128))
    fb_trans = str.maketrans('01', 'FB')
    fb_dict = {s.translate(fb_trans):i for i, s in enumerate(fb_list)}
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
            part_2 = seat_id -1
            break
        else:
            part_2 += 1

    return part_1, part_2


day5_test_values = {"FBFBBFFRLR": (357, any),
                    "BFFFBBFRRR": (567, any),
                    "FFFBBBFRRR": (119, any),
                    "BBFFBBFRLL": (820, any),
                    }

def day6(input_values : str) -> tuple:
    """template"""
    part_1 = 0
    part_2 = 0
    ...
    groups = input_values.split('\n\n')

    for group in groups:
        person_yesses = [set(person.strip()) for person in group.split('\n')]
        all_yesses = person_yesses[0].intersection(*person_yesses)
        part_2 += len(all_yesses)
        group_yesses = set(group.replace('\n', ''))
        print(group_yesses)
        part_1 += len(group_yesses)


    return part_1, part_2

day6_test_values = {"abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb": (11, 6),
                    }

def dayx(input_values : list) -> tuple:
    """template"""
    part_1 = None
    part_2 = None
    ...

    return part_1, part_2

if __name__ == '__main__':
    today = date.today()
    if today.month == 12:
        print('Merry Christmas')
    for input_value, answer in day6_test_values.items():
        try:
            assert answer == day6(input_value)
        except Exception as e:
            print(input_value, answer, day6([input_value, ]))
            raise e
    with open('input/day6.txt') as f:
        input_values = f.read()
    print(day6(input_values))
