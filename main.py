import re
from collections import deque, defaultdict, Counter
from copy import copy
from datetime import date
from itertools import permutations
from operator import add, sub, mul, truediv


class Anything():
    """Anything object as a substitute for the as-yet unknown answer to a question during testing """

    def __eq__(self, other):
        return True

    def __repr__(self):
        return "<Anything object> : always returns True"


anything = Anything()

test_values = {}


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


test_values[5] = {"FBFBBFFRLR": (357, anything),
                  "BFFFBBFRRR": (567, anything),
                  "FFFBBBFRRR": (119, anything),
                  "BBFFBBFRLL": (820, anything),
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


test_values[6] = {"abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb": (11, 6),
                  }


def day7(input_values: str) -> tuple:
    """Build a graph of bags, find the set of unique parents, recursively find children"""

    def number_of_children(bag) -> int:
        """recursively find the number of child bags"""
        nonlocal bags
        children = 0
        for child_bag, number in bags[bag].items():
            children += number * (number_of_children(child_bag) + 1)
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
        contents = {bag[2:]: int(bag[0]) for bag in contents.split(', ')}
        bags[container] = contents
    print(bags)
    can_contain = ['shiny gold bag', ]
    for target in can_contain:
        for bag in bags.keys():
            if target in bags[bag].keys():
                can_contain.append(bag)

    print(can_contain)
    part_1 = len(set(can_contain)) - 1
    part_2 = number_of_children('shiny gold bag')
    return part_1, part_2


test_values[7] = {
    """light red bags contain 1 bright white bag, 2 muted yellow bags.\ndark orange bags contain 3 bright white bags, 4 muted yellow bags.\nbright white bags contain 1 shiny gold bag.\nmuted yellow bags contain 2 shiny gold bags, 9 faded blue bags.\nshiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.\ndark olive bags contain 3 faded blue bags, 4 dotted black bags.\nvibrant plum bags contain 5 faded blue bags, 6 dotted black bags.\nfaded blue bags contain no other bags.\ndotted black bags contain no other bags.""": (
        4, 32),
    """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""": (anything, 126)
}


def day8(input_values: str) -> tuple:
    """Boot loader"""

    def parse(cmd, val):
        if cmd == 'acc':
            return val, 1
        elif cmd == 'jmp':
            return 0, val
        elif cmd == 'nop':
            return 0, 1
        print(cmd)
        raise NotImplementedError

    commands = input_values.splitlines()
    part_1 = 0
    executed = set()
    index = 0
    while True:
        command, value = commands[index].split(' ')
        increment, jump = parse(command, int(value))
        index += jump
        if index in executed:
            break
        part_1 += increment
        executed.add(index)

    for i, line in enumerate(commands):
        modified_commands = copy(commands)
        switch = {'nop': 'jmp', 'jmp': 'nop'}
        if (cmd := line[:3]) != 'acc':
            modified_commands[i] = switch[cmd] + line[3:]
        else:
            continue
        executed = set()
        index = 0
        part_2 = 0
        while True:
            command, value = modified_commands[index].split(' ')
            increment, jump = parse(command, int(value))
            part_2 += increment
            index += jump
            if index in executed:
                break
            elif index >= len(commands):
                return part_1, part_2

            executed.add(index)


test_values[8] = {"""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""": (5, 8),
                  }


def day9(input_values: str) -> tuple:
    """template"""
    part_1 = None
    numbers = [int(line) for line in input_values.splitlines()]
    if len(input_values) < 1000:
        preamble = 5  # test data
    else:
        preamble = 25  # real data
    chunk = deque(maxlen=preamble)
    for num in numbers:
        if part_1:
            break
        if len(chunk) == preamble:
            for num1 in chunk:
                if (num - num1) in chunk:
                    break
            else:
                part_1 = num
                break
        chunk.append(num)

    mini_maxi_sums = []
    for num in numbers:
        for i, mms in enumerate(mini_maxi_sums):
            mini, maxi, summ = mms
            if summ == part_1:
                part_2 = mini + maxi
                return part_1, part_2
            mini_maxi_sums[i] = (min(mini, num), max(maxi, num), summ + num)
        mini_maxi_sums.append((num, num, num))


test_values[9] = {"""35\n20\n15\n25\n47\n40\n62\n55\n65\n95\n102\n117
150\n182\n127\n219\n299\n277\n309\n576
""": (127, 62),
                  }


def day10(input_values: str) -> tuple:
    """build list of joltages and differences"""
    jolts = [0, ] + sorted(int(x) for x in input_values.splitlines())
    jolts.append(jolts[-1] + 3)
    difs = [j1 - j0 for j0, j1 in zip(jolts[:-1], jolts[1:])]
    part_1 = difs.count(1) * difs.count(3)

    # Dynamic programming approach
    combos = {0: 1}
    for j in jolts[1:]:
        combo = 0
        for joltage in range(max(0, j - 3), j):
            if joltage in jolts:
                combo += combos[joltage]
        combos[j] = combo
    part_2 = combos[max(jolts)]

    return part_1, part_2


test_values[10] = {"""16
10
15
5
1
11
7
19
6
12
4""": (35, 8),
                   }


def day11(input_values: str) -> tuple:
    """template"""
    part_1 = None
    part_2 = None
    grid = {(x, y): val for (y, row) in enumerate(input_values.splitlines()) for (x, val) in enumerate(row)}
    grid_2 = grid.copy()
    new_grid = {}
    indices = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while new_grid != grid:
        if new_grid:
            grid = new_grid.copy()
        for (x, y), val in grid.items():
            if val in 'L#':
                neighbours = sum([grid.get((x + i, y + j), '.') == '#' for i, j in indices])
            if val == 'L' and neighbours == 0:
                new_grid[(x, y)] = '#'
            elif val == '#' and neighbours >= 4:
                new_grid[(x, y)] = 'L'
            else:
                new_grid[(x, y)] = val

    part_1 = list(new_grid.values()).count('#')

    def seen(pt, direction, grid):
        x, y = pt
        i, j = direction
        if (obj := grid.get((x + i, y + j), 'L')) in '#L':  # Treat surrounding squares as empty seats
            return obj
        else:
            return seen((x + i, y + j), (i, j), grid)

    new_grid_2 = {}
    while new_grid_2 != grid_2:
        if new_grid_2:
            grid_2 = new_grid_2.copy()
        for (x, y), val in grid_2.items():
            if val in 'L#':
                visible = sum([seen((x, y), (i, j), grid_2) == '#' for i, j in indices])
            if val == 'L' and visible == 0:
                new_grid_2[(x, y)] = '#'
            elif val == '#' and visible >= 5:
                new_grid_2[(x, y)] = 'L'
            else:
                new_grid_2[(x, y)] = val

    part_2 = list(new_grid_2.values()).count('#')
    return part_1, part_2


test_values[11] = {"""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""": (37, 26),
                   }


def day12(input_values: str) -> tuple:
    """We are sailing"""
    part_2 = None
    instructions = ((x[0], int(x[1:])) for x in input_values.splitlines())
    current_direction = 90  # East
    easting, northing = 0, 0
    for move, distance in instructions:
        if move == 'L':
            current_direction -= distance
        elif move == 'R':
            current_direction += distance
        current_direction %= 360
        if move == 'F':
            move = {0: 'N', 90: 'E', 180: 'S', 270: 'W'}[current_direction]
        if move == 'N':
            northing += distance
        if move == 'S':
            northing -= distance
        if move == 'E':
            easting += distance
        if move == 'W':
            easting -= distance
    part_1 = abs(easting) + abs(northing)

    instructions = ((x[0], int(x[1:])) for x in input_values.splitlines())
    waypoint_easting = 10
    waypoint_northing = 1
    easting, northing = 0, 0
    for move, distance in instructions:
        if move in 'LR' and distance == 180:
            waypoint_easting, waypoint_northing = -waypoint_easting, -waypoint_northing
        elif (move, distance) in (('L', 90), ('R', 270)):
            waypoint_easting, waypoint_northing = -waypoint_northing, waypoint_easting
        elif (move, distance) in (('R', 90), ('L', 270)):
            waypoint_easting, waypoint_northing = waypoint_northing, -waypoint_easting
        if move == 'F':
            easting += distance * waypoint_easting
            northing += distance * waypoint_northing
        if move == 'N':
            waypoint_northing += distance
        if move == 'S':
            waypoint_northing -= distance
        if move == 'E':
            waypoint_easting += distance
        if move == 'W':
            waypoint_easting -= distance

    part_2 = abs(easting) + abs(northing)

    return part_1, part_2


test_values[12] = {"""F10
N3
F7
R90
F11""": (25, 286),
                   }


def day13(input_values: str) -> tuple:
    """template"""
    part_1 = None
    part_2 = None
    timestamp, busses = input_values.splitlines()
    timestamp = int(timestamp)
    busses = set(busses.split(','))
    busses.remove('x')
    part_1_busses = map(int, busses)
    part_1 = min(((bus - timestamp % bus), bus) for bus in part_1_busses)
    bus = part_1[1]
    part_1 = bus * (bus - timestamp % bus)
    busses = [x for x in input_values.splitlines()[1].split(',')]
    busses = sorted([(int(bus), i) for i, bus in enumerate(busses) if bus != 'x'],
                    reverse=True,
                    )
    if (7, 0) in busses:
        big_bus, big_int = busses.pop(0)
        part_2 = 0 - big_int
    else:
        big_bus, big_int = 641 * 13 * 17 * 29 * 37, 13
        part_2 = - 13
    while True:
        part_2 += big_bus
        if all((part_2 + i) % bus == 0 for bus, i in busses):
            break

    return part_1, part_2


test_values[13] = {"""939
7,13,x,x,59,x,31,19""": (295, 1068781),
                   }


def day14(input_values: str) -> tuple:
    """Bitmasks"""

    def parse_chunks(data: str):
        mask, values = "", []
        for line in data.splitlines():
            if line[:4] == 'mask':
                if mask:
                    yield mask, values
                mask = line[7:]
                values = []
            else:
                m = re.match(r"mem\[(\d+)\] = (\d+)", line)
                address = int(m.group(1))
                value = int(m.group(2))
                values.append((address, value))
        yield mask, values

    register = dict()
    for bitmask, values in parse_chunks(input_values):
        for address, value in values:
            binary_value = bin(value)[2:].zfill(36)
            output = []
            for mi, vi in zip(bitmask[::-1], binary_value[::-1]):
                if mi in '01':
                    output.append(mi)
                else:
                    output.append(vi)
            register[address] = int("".join(output[::-1]), 2)
    part_1 = sum(register.values())

    def append_all(l, i):
        for sublist in l:
            sublist.append(i)

    register = dict()
    for bitmask, values in parse_chunks(input_values):
        for address, value in values:
            binary_value = bin(value)[2:].zfill(36)
            output = [[]]
            for mi, vi in zip(bitmask[::-1], binary_value[::-1]):
                if mi == '0':
                    append_all(output, vi)
                if mi == '1':
                    append_all(output, mi)
                else:
                    extra_output = output.copy()
                    append_all(output, '0')
                    append_all(extra_output, '1')
                    output.extend(extra_output)
            register[address] = int("".join(output[::-1]), 2)
    part_2 = sum(register.values())

    return part_1, part_2


test_values[14] = {"""mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""": (165, anything),
                   """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""": (anything, 208)
                   }


def day15(input_values: str) -> tuple:
    """Off by one error generator"""
    numbers = [int(x) for x in input_values.split(',')]
    seen = {n: i for i, n in enumerate(numbers[:-1], 1)}
    turn = len(numbers)
    n = numbers[-1]
    while turn < 2020:
        say = turn - seen.get(n, turn)
        seen[n] = turn
        n = say
        turn += 1
    part_1 = n
    while turn < 30000000:
        say = turn - seen.get(n, turn)
        seen[n] = turn
        n = say
        turn += 1

    part_2 = n
    return part_1, part_2


test_values[15] = {"""0,3,6""": (436, 175594),
                   "1,3,2": (1, 2578),
                   "2,1,3": (10, 3544142),
                   "1,2,3": (27, 261214),
                   "2,3,1": (78, 6895259),
                   "3,2,1": (438, 18),
                   "3,1,2": (1836, 362),
                   }


def day16(input_values: str) -> tuple:
    """Follow the rules"""
    rules, my_numbers, other_numbers = [section.splitlines() for section in input_values.split('\n\n')]
    rule = defaultdict(set)
    part_1_valid = set()

    for r in rules:
        name, a, b, c, d = re.findall(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', r)[0]
        a, b, c, d = int(a), int(b), int(c), int(d)
        for i in range(a, b + 1):
            rule[name].add(i)
            part_1_valid.add(i)
        for i in range(c, d + 1):
            rule[name].add(i)
            part_1_valid.add(i)
    part_1 = sum(int(i) for ticket in other_numbers[1:] for i in ticket.split(',') if int(i) not in part_1_valid)
    valid_tickets = [x for x in other_numbers[1:] if all(int(num) in part_1_valid for num in x.split(','))]
    field_numbers = [set() for _ in valid_tickets[0].split(',')]
    # Get all ticket numbers in each field position
    for ticket in valid_tickets:
        [nums.add(int(num)) for nums, num in zip(field_numbers, ticket.split(','))]

    # Determine which field names are possible for each position
    possible_names = [set(rule.keys()) for _ in range(len(field_numbers))]
    for i, field in enumerate(field_numbers):
        for field_name, valid_values in rule.items():
            if field.difference(valid_values):
                possible_names[i].discard(field_name)

    while any(len(x) > 1 for x in possible_names):
        for subset in possible_names:
            if len(subset) == 1:
                field_name = subset.pop()
                [x.discard(field_name) for x in possible_names]
                subset.add(field_name)

    part_2 = 1
    my_numbers = [int(x) for x in my_numbers[1].split(',')]
    for num, field_name in zip(my_numbers, possible_names):
        if 'departure' in field_name.pop():
            part_2 *= num
    return part_1, part_2


test_values[16] = {"""class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""": (71, anything),
                   }


def day17(input_values: str) -> tuple:
    """Conway Cubes.  based on a solution for Rhino 3D"""
    part_1 = conway(input_values, dimensions=3)

    part_2 = conway(input_values, dimensions=4)

    return part_1, part_2


def conway(input_values, dimensions):
    new_cubes = set()
    # Build the starting grid
    for y, row in enumerate(input_values.splitlines()):
        for x, cell in enumerate(row):
            if cell == '#':
                new_cubes.add((x, y) + (0,) * (dimensions - 2))
    # Initialise sets and lists
    old_spheres = []
    neighbouring = set(permutations([1, 0, -1] * dimensions, dimensions))
    neighbouring.remove((0,) * dimensions)  # a cube is not its own neighbour
    for round in range(6 + 1):
        cubes = new_cubes.copy()
        neighbours = defaultdict(int)
        old_spheres = set()
        answer = 0

        # Draw cubes and identify neighbours
        for cube in cubes:
            answer += 1
            for n in neighbouring:
                neighbours[tuple(cube[i] + n[i] for i in range(dimensions)
                                 )] += 1
        new_cubes = set()

        # Apply rules for creation of cubes in next round
        for location, n in neighbours.items():
            if location in cubes:
                if 2 <= n <= 3:
                    new_cubes.add(location)
            elif n == 3:
                new_cubes.add(location)
    return answer


test_values[17] = {""".#.
..#
###""": (112, 848),
                   }


def day18(input_values: str) -> tuple:
    """Map operators to overloaded methods in order to achieve the desired operation order
    TODO : Work out why the brace parser does not work"""

    class Number:
        """With overloaded operators"""

        def __init__(self, n):
            self.value = n

        def __mul__(self, other):
            return Number(self.value + other.value)

        def __add__(self, other):
            return Number(self.value * other.value)

        def __truediv__(self, other):
            return Number(self.value * other.value)

    # create a number object for each digit 0-9
    for i in range(10):
        locals()[f'n{i}'] = Number(i)

    # build translation tables for parts 1 and 2
    # part 1 : same precedence
    t1 = {i: 'n' + i for i in '0123456789'}
    t1['*'] = '/'
    t1['+'] = '*'
    part_1_trans = str.maketrans(t1)
    # part 2 : + before *
    t2 = {i: 'n' + i for i in '0123456789'}
    t2['+'] = '*'
    t2['*'] = '+'
    part_2_trans = str.maketrans(t2)

    part_1 = 0
    part_2 = 0
    for line in input_values.splitlines():
        part_1 += eval(line.translate(part_1_trans)).value
        part_2 += eval(line.translate(part_2_trans)).value

    return part_1, part_2


def eval_parser(formula):
    """Works for part 1 - not used"""
    p = iter(formula.replace(' ', ''))
    new_val = None
    past_val = None
    operation = None
    braces = 0
    ops = {'+': add,
           '*': mul,
           }  # No subtraction or division
    for c in p:
        if c.isdigit():
            new_val = int(c)
        elif c in '+-*/':
            operation = ops[c]
        elif c == ('('):
            braces += 1
            sub_formula = [c, ]
            while braces:
                c = next(p)
                if c == '(':
                    braces += 1
                elif c == ')':
                    braces -= 1
                sub_formula.append(c)
            new_val = eval_parser(''.join(sub_formula[1:-1]))
        if new_val:
            if past_val:
                past_val = operation(past_val, new_val)
            else:
                past_val = new_val
            new_val = None
    return past_val


def brace_parser(line):
    """Does not work - not uses"""
    parser = []
    parentheses = [0]
    for c in line[::-1]:
        if c.isdigit():
            parser.append(')')
            parentheses[-1] += 1
        elif c == '(':
            parser.append('(' * parentheses.pop())
        elif c == ')':
            parentheses.append(0)
        parser.append(c)
    parser.append('(' * parentheses.pop())
    expression = "".join(parser[::-1])
    return expression


test_values[18] = {"""1 + 2 * 3 + 4 * 5 + 6""": (71, 231),
                   """1 + (2 * 3) + (4 * (5 + 6))""": (51, 51),
                   """2 * 3 + (4 * 5)""": (26, 46),
                   """5 + (8 * 3 + 9 + 3 * 4 * 3)""": (437, 1445),
                   """5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))""": (12240, 669060),
                   """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""": (13632, 23340),
                   }


def day20(input_values: str) -> tuple:
    """template"""
    part_1 = 1
    part_2 = None

    tiles = {int(tile[5:9]): tile.splitlines()[1:] for tile in input_values.strip().split('\n\n')}
    edges = {n: [tile[0], tile[-1], ''.join([l[0] for l in tile]), ''.join([l[-1] for l in tile])] for n, tile in
             tiles.items()}
    print(edges)
    for n, edgelist in edges.items():
        edges[n] = [min(edge, edge[::-1]) for edge in edgelist]
    edge_counter = Counter(edge for edgelist in edges.values() for edge in edgelist)

    print(edges)
    print(edge_counter)
    for n, edgelist in edges.items():
        if len([edge for edge in edgelist if edge_counter[edge] == 1]) == 2:
            part_1 *= n

    return part_1, part_2


test_values[20] = {"""Tile 2311:\n..##.#..#.\n##..#.....\n#...##..#.\n####.#...#\n##.##.###.\n##...#.###\n.#.#.#..##\n..#....#..\n###...#.#.\n..###..###

Tile 1951:\n#.##...##.\n#.####...#\n.....#..##\n#...######\n.##.#....#\n.###.#####\n###.##.##.\n.###....#.\n..#.#..#.#\n#...##.#..

Tile 1171:\n####...##.\n#..##.#..#\n##.#..#.#.\n.###.####.\n..###.####\n.##....##.\n.#...####.\n#.##.####.\n####..#...\n.....##...

Tile 1427:\n###.##.#..\n.#..#.##..\n.#.##.#..#\n#.#.#.##.#\n....#...##\n...##..##.\n...#.#####\n.#.####.#.\n..#..###.#\n..##.#..#.

Tile 1489:\n##.#.#....\n..##...#..\n.##..##...\n..#...#...\n#####...#.\n#..#.#.#.#\n...#.#.#..\n##.#...##.\n..##.##.##\n###.##.#..

Tile 2473:\n#....####.\n#..#.##...\n#.##..#...\n######.#.#\n.#...#.#.#\n.#########\n.###.#..#.\n########.#\n##...##.#.\n..###.#.#.

Tile 2971:\n..#.#....#\n#...###...\n#.#.###...\n##.##..#..\n.#####..##\n.#..####.#\n#..#.#..#.\n..####.###\n..#.#.###.\n...#.#.#.#

Tile 2729:\n...#.#.#.#\n####.#....\n..#.#.....\n....#..#.#\n.##..##.#.\n.#.####...\n####.#.#..\n##.####...\n##..#.##..\n#.##...##.

Tile 3079:\n#.#.#####.\n.#..######\n..#.......\n######....\n####.#..#.\n.#...#.##.\n#.#####.##\n..#.###...\n..#.......\n..#.###...""": (
    20899048083289, anything),
}


def day21(input_values: str) -> tuple:
    """template"""
    part_1 = 0
    part_2 = None
    allergen_containers = defaultdict(set)
    all_foods = Counter()
    all_allergens = set()
    for line in input_values.splitlines():
        foods, allergens = line.split(' (')
        foods = foods.split()
        all_foods.update(foods)
        for food in foods:
            for allergen in allergens:
                allergen_containers[allergen]
        allergens = allergens.replace(',', '')[:-1].split()[1:]
        all_allergens.update(allergens)
    print(all_foods, all_allergens)

    return part_1, part_2


test_values[21] = {"""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""": (5, anything),
                   }


def day22(input_values: str) -> tuple:
    """Cards with crab"""

    def simple_round(hand_1, hand_2) -> tuple:
        if hand_1[0] > hand_2[0]:
            return 1, 2
        return 2, 1

    player_1, player_2 = [deque([int(x) for x in section.splitlines()[1:]]) for section in input_values.split('\n\n')]
    player = {1: player_1,
              2: player_2}
    while player[1] and player[2]:
        winner, loser = simple_round(player[1], player[2])
        player[winner].append(player[winner].popleft())
        player[winner].append(player[loser].popleft())
    part_1 = sum([card * i for i, card in enumerate(reversed(player[winner]), 1)])

    def recursive_round(hand_1, hand_2, seen) -> tuple:
        player = {1: hand_1, 2: hand_2}
        while hand_1 and hand_2:
            print(hand_1, hand_2)
            if (hands := (tuple(hand_1), tuple(hand_2))) in seen:
                print("seen it", hand_1)
                return ("Seen", 0)
            seen.add(hands)
            card = {}
            card[1], card[2] = hand_1.popleft(), hand_2.popleft()
            if (card[1] <= len(hand_1)) and (card[2] <= len(hand_2)):
                winner, loser = recursive_round(deque(list(hand_1)[:card[1]]), deque(list(hand_2)[:card[2]]),
                                                seen.copy())
            elif card[1] > card[2]:
                winner, loser = 1, 2
            else:
                winner, loser = 2, 1
            if winner == "Seen":
                return "Seen", 0
            player[winner].append(card[winner])
            player[winner].append(card[loser])
        return winner, loser

    seen = set()

    player_1, player_2 = [deque([int(x) for x in section.splitlines()[1:]]) for section in input_values.split('\n\n')]
    player = {1: player_1,
              2: player_2}
    winner, loser = recursive_round(player_1, player_2, seen)
    if winner == "Seen":
        winner = 1
        player[1].append(player_1.popleft())
        player[1].append(player_2.popleft())
    print("Winner : ", player[winner])
    part_2 = sum([card * i for i, card in enumerate(reversed(player[winner]), 1)])

    return part_1, part_2


test_values[22] = {"""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""": (306, 291),
                   }


def day23(input_values: str) -> tuple:
    """template"""

    circle = deque(map(int, input_values))
    for move in range(1, 101):
        current = circle[0]

        circle.rotate(-1)
        pick_up = [circle.popleft() for _ in range(1, 4)]
        destination = (current - 1) % 10
        while (destination in pick_up) or destination <= 0:
            destination -= 1
            if destination <= 0:
                destination = 9
        print(f"""
-- move {move} --
cups:  {circle} 
current: {current}
pick up: {pick_up}
destination: {destination}
""")

        circle.rotate(-circle.index(destination) - 1)
        circle.extendleft(pick_up[::-1])
        circle.rotate(-(circle.index(current)) - 1)
    circle.rotate(-circle.index(1))
    circle.popleft()
    part_1 = int("".join(map(str, circle)))

    circle = deque(map(int, input_values))
    circle.extend(range(10, 1_000_001))
    circle_copy = list(circle)
    for move in range(1, 10_000_001):
        current = circle[0]

        circle.rotate(-1)
        pick_up = [circle.popleft() for _ in range(1, 4)]
        destination = (current - 1) % 1_000_000
        while (destination in pick_up) or destination <= 0:
            destination -= 1
            if destination <= 0:
                destination = 1_000_000

        circle.rotate(-circle.index(destination) - 1)
        circle.extendleft(pick_up[::-1])
        circle.rotate(-(circle.index(current)) - 1)
    circle.rotate(-circle.index(1))
    circle.popleft()

    part_2 = circle.popleft() * circle.popleft()
    ...

    return part_1, part_2


test_values[23] = {"""389125467""": (67384529, 149245887792),
                   }


def day24(input_values: str) -> tuple:
    """Flipping tiles - a bit complex"""
    lines = input_values.splitlines()
    directions = {'e': complex(1, 0),
                  'se': complex(0.5, -0.5),
                  'sw': complex(-0.5, -0.5),
                  'w': complex(-1, 0),
                  'nw': complex(-0.5, 0.5),
                  'ne': complex(0.5, 0.5),
                  }
    visited = Counter()
    for line in lines:
        line = list(reversed(line))
        position = complex(0, 0)
        while line:
            move = line.pop()
            if move not in directions:
                move += line.pop()
            position += directions[move]
        visited.update([position, ])
    black = [k for k, v in visited.items() if v % 2]
    part_1 = len(black)

    for day in range(100):
        day_flips = set()
        neighbouring_tiles = set()
        for tile in visited.keys():
            for neighbour in directions.values():
                if (tile + neighbour) not in visited:
                    new = tile + neighbour
                    neighbouring_tiles.add(new)
        [visited.setdefault(key, 0) for key in neighbouring_tiles]
        for tile, visits in visited.items():
            is_black = (visits % 2)
            black_neighbours = 0
            for neighbour in directions.values():
                if (visited.get(tile + neighbour, 0) % 2):
                    black_neighbours += 1
            if is_black and black_neighbours not in (1, 2):
                day_flips.add(tile)
            elif not is_black and black_neighbours == 2:
                day_flips.add(tile)
        visited.update(day_flips)
        black = [k for k, v in visited.items() if v % 2]

    part_2 = len(black)

    return part_1, part_2


test_values[24] = {"""sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""": (10, 2208),
                   }


def day25(input_values: str) -> tuple:
    """template"""
    card_key, door_key = [int(x) for x in input_values.splitlines()]
    subject_number = 7

    card_public_key = 1
    card_loop = 0
    while card_public_key != card_key:
        card_public_key *= subject_number
        card_public_key %= 20201227
        card_loop += 1

    door_public_key = 1
    door_loop = 0

    while door_public_key != door_key:
        door_public_key *= subject_number
        door_public_key %= 20201227
        door_loop += 1

    encryption_key = 1
    for _ in range(door_loop):
        encryption_key *= card_public_key
        encryption_key %= 20201227

    part_1 = encryption_key
    part_2 = None
    ...

    return part_1, part_2


test_values[25] = {"""5764801
17807724""": (14897079, anything),
                   }


def day(input_values: str) -> tuple:
    """template"""
    part_1 = None
    part_2 = None
    ...

    return part_1, part_2


test_values[0] = {"""""": (anything, anything),
                  }

if __name__ == '__main__':
    today = date.today()
    day = 22
    day_function = eval(f'day{day}')
    if today.month == 12:
        print('Merry Christmas')
    print(f'https://adventofcode.com/2020/day/{day}')
    for input_value, answer in test_values[day].items():
        try:
            assert answer == day_function(input_value)
            print(answer, 'Test Passed')
        except Exception as e:
            print(input_value, answer, day_function(input_value, ))
            raise e
    try:
        with open(f'input/day{day}.txt') as f:
            input_values = f.read()
    except FileNotFoundError:
        print(f"https://adventofcode.com/2020/day/{day}/input")
    print(day_function(input_values))
