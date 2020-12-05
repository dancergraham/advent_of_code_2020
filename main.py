from datetime import date


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

    for boarding_pass in input_values:
        row = fb_dict[boarding_pass.strip()[:7]]
        column = lr_dict[boarding_pass.strip()[7:]]
        seat_id = (8 * row) + column
        part_1 = max(part_1, seat_id)
    return part_1, part_2


day5_test_values = {"FBFBBFFRLR": 357,
                    "BFFFBBFRRR": 567,
                    "FFFBBBFRRR": 119,
                    "BBFFBBFRLL": 820,
                    }

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    today = date.today()
    if today.month == 12:
        print('Merry Christmas')
    with open('input/day5.txt') as f:
        input_values = f.readlines()
    for input_value, answer in day5_test_values.items():
        try:
            assert day5([input_value, ]) == (answer, None)
        except Exception as e:
            print(input_value, answer, day5([input_value, ]))
            raise e
    print(day5(input_values))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
