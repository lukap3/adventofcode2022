from collections import deque

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day20/example.txt": [3, 1623178306]}
    data_file = "data/day20/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i, line in enumerate(data):
            data[i] = int(line)
        return data

    @staticmethod
    def move(d, el):
        idx = d.index(el)
        d.rotate(-idx)
        _, v = d.popleft()
        d.rotate(-v)
        d.appendleft(el)

    def mix(self, d, rounds=1):
        original = d.copy()
        for _ in range(rounds):
            for el in original:
                self.move(d, el)
        while d[0][1] != 0:
            d.rotate(-1)
        return d

    def part_1_logic(self, numbers):
        numbers = deque(enumerate(numbers))
        numbers = self.mix(numbers)
        return sum(numbers[n % len(numbers)][1] for n in (1000, 2000, 3000))

    def part_2_logic(self, numbers):
        numbers = [n * 811589153 for n in numbers]
        numbers = deque(enumerate(numbers))
        numbers = self.mix(numbers, rounds=10)
        return sum(numbers[n % len(numbers)][1] for n in (1000, 2000, 3000))


day = Day()
