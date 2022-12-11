import re

from advent_day import AdventDay


class Monkey:
    def __init__(self, idx, items, operation, test, t, f):
        self.idx = idx
        self.items = items
        self.operation = operation
        self.test = test
        self.t = t
        self.f = f
        self.inspections = 0

    @staticmethod
    def apply_operation(num, operation):
        operation = operation[5:]
        operation_eval = operation.replace("old", f"int({num})")
        return eval(operation_eval)

    def check_test(self, num):
        return num % self.test == 0

    def execute(self, monkeys, div=True, m=None):
        self.inspections += len(self.items)

        # inspec all items
        for i in range(len(self.items)):
            # apply operation to item
            self.items[i] = self.apply_operation(self.items[i], self.operation)

            # divide by 3 and round down
            if div:
                self.items[i] = int(self.items[i] / 3)

            # test
            chk = self.check_test(self.items[i])

            # lower the worry level using m
            if m is not None:
                self.items[i] = self.items[i] % m

            # throw based on test
            if chk:
                monkeys[self.t].items += [self.items[i]]
            else:
                monkeys[self.f].items += [self.items[i]]
        self.items = []

    def to_str(self):
        name = f"Monkey {self.idx}:"
        items = f"Starting items: {self.items}"
        operation = f"Operation: {self.operation}"
        test = f"Test: divisible by {self.test}"
        t_statement = f"If true: throw to monkey {self.t}"
        f_statement = f"If false: throw to monkey {self.f}"
        return f"""{name}
            {items}
            {operation}
            {test}
                {t_statement}
                {f_statement}"""


class Day(AdventDay):
    test_files = {"data/day11/example.txt": [10605, 2713310158]}
    data_file = "data/day11/data.txt"

    def parse_file(self, data):
        blocks = [[]]
        data = data.split("\n")[:-1]
        idx = 0
        for line in data:
            if line == "":
                idx += 1
                blocks.append([])
            else:
                blocks[idx].append(line)

        monkeys = []
        for block in blocks:
            idx = re.search("Monkey (\d+):", block[0]).groups()
            idx = int(idx[0])

            items = re.findall("(\d+)", block[1])
            items = [int(item) for item in items]

            operation = block[2].split(": ")[1]

            test = re.findall("(\d+)", block[3])
            test = int(test[0])

            t = int(re.findall("(\d+)", block[4])[0])
            f = int(re.findall("(\d+)", block[5])[0])
            monkeys.append(Monkey(idx, items, operation, test, t, f))

        return monkeys

    def part_1_logic(self, monkeys):
        for _ in range(20):
            for monkey in monkeys:
                monkey.execute(monkeys)

        inspections = [monkey.inspections for monkey in monkeys]
        inspections = sorted(inspections, reverse=True)

        return inspections[0] * inspections[1]

    def part_2_logic(self, monkeys):
        m = 1
        for monkey in monkeys:
            m *= monkey.test

        for _ in range(10000):
            for monkey in monkeys:
                monkey.execute(monkeys, div=False, m=m)

        inspections = [monkey.inspections for monkey in monkeys]
        inspections = sorted(inspections, reverse=True)

        return inspections[0] * inspections[1]


day = Day()
