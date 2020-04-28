import sys
from random import seed, randint
from typing import List
probabilities = []
ignore = set()


def init(args: List[str]):
    global probabilities
    global ignore
    try:
        probabilities = eval(args[1])
        for num in probabilities:
            if type(num) != int or num < 0:
                print("Must be a list of non-negative integers")
                return False
        if sum(probabilities) < 1:
            print("Invalid probabilities")
            return False
        if int(args[0]) > 1000000:
            print("That would take a really long time")
            return False
        args = args[2:]
        if len(args) > len(probabilities):
            print("Can't ignore more months that given probabilities")
            return False
        else:
            month_set = set(range(len(probabilities)))
            ignore = set(map(int, args))
            if ignore == month_set:
                print("Can't ignore every month")
                return False
            if len(ignore - month_set) != 0:
                print("Invalid month index")
                return False
            for idx in month_set - ignore:
                if probabilities[idx] != 0:
                    break
            else:
                print("Can't only count months with no births")
                return False
            seed()
            return True
    except ValueError:
        print("Invalid argument, must be a number")
        return False
    except SyntaxError:
        print("Please format probabilty list as: [x,y,z]")
        return False


def main(iterations: int):
    print(sorted(simulate()
                 for itertaion in range(iterations))[iterations//2] + 1)


def simulate():
    months = [[False for day in range(30)]
              for month in range(len(probabilities))]
    people = 0
    while True:
        people += 1
        if birth_person(months):
            return people


def birth_person(months: List[List[bool]]) -> bool:
    month = randint(1, sum(probabilities))
    for idx, prob in enumerate(probabilities):
        month -= prob
        if month <= 0:
            day = randint(0, 29)
            if months[idx][day] and idx not in ignore:
                return True
            else:
                months[idx][day] = True
                return False
    return


if __name__ == "__main__":
    if init(sys.argv[1:]):
        main(int(sys.argv[1]))
