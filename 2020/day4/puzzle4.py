import re
def validPassport(p):

    keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    for k in keys:
        if k not in p:
            return False

    conditions = [
        1920 <= int(keys['byr']) <= 2002,
        2010 <= int(keys['iyr']) <= 2020,
        2020 <= int(keys['eyr']) <= 2030
    
    ]


with open("input.txt", "r") as f:

    lines = f.readlines()

    passports = []
    while len(lines) > 0:

        curr = []
        while len(lines) > 0 and (l := lines.pop(0)) != '\n':

            matches = re.findall("([a-z]{3}):([0-9]*)(cm|in)?|(#[0-9a-z]*)|([a-z]*)", l)

            print(matches)

            curr.extend(l)

        passports.append(dict(curr))

    valid = 0

    