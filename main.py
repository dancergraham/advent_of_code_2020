from datetime import date

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
    

def aocday3():
    with open('input/day3.txt') as f:
        input_data = [list(line.strip()) for line in f.readlines()]
    product =1
    answers = {}
    for dx, dy in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
        answer, x, y = 0,0,0
        while True:
            x = (x + dx) % len(input_data[0])
            y += dy
            try:
                answer += (input_data[y][x] == '#')

            except IndexError:
                answers[(dx,dy)] = answer
                product *= answer
                break
    part_1 = answers[(3,1)]
    return part_1, product


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    today = date.today()
    if today.month == 12:
        print('Merry Christmas')
    print(day2())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
