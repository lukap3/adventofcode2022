import string

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day3/example.txt": [157, 70]}
    data_file = "data/day3/data.txt"

    letters = string.ascii_lowercase + string.ascii_uppercase

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        return data

    def part_1_logic(self, data):
        priority_sum = 0
        for i in range(len(data)):
            h = int(len(data[i]) / 2)
            cs = []
            for char in data[i][0:h]:
                if char in data[i][h:]:
                    cs.append(char)
                    priority_sum += 1 + self.letters.index(char)
                    break
        return priority_sum

    def part_2_logic(self, data):
        groups, badges = [], []
        priority_sum = 0
        while data:
            groups.append([data.pop(), data.pop(), data.pop()])
        for group in groups:
            for char in group[0]:
                if char in group[1] and char in group[2]:
                    priority_sum += 1 + self.letters.index(char)
                    badges.append(char)
                    break
        return priority_sum


day = Day()
