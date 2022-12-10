from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day10/example.txt": [13140, 124]}
    data_file = "data/day10/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        return data

    @staticmethod
    def update_cycle(x, cycle, read_cycles):
        cycle += 1
        if cycle in read_cycles:
            read_cycles[cycle] = x
        return cycle, read_cycles

    def part_1_logic(self, data):
        x = 1
        cycle = 1
        read_cycles = {20: 0, 60: 0, 100: 0, 140: 0, 180: 0, 220: 0}
        for i, line in enumerate(data):
            line = line.split(" ")
            if line[0] == "addx":
                cycle, read_cycles = self.update_cycle(x, cycle, read_cycles)
                x += int(line[1])
            cycle, read_cycles = self.update_cycle(x, cycle, read_cycles)

        signal_sum = sum([key * value for key, value in read_cycles.items()])
        return signal_sum

    @staticmethod
    def draw(crt, cycle, x):
        if abs(x - (cycle % 40)) <= 1:
            crt[cycle] = "■"
        return crt

    def part_2_logic(self, data):
        crt = list(" " * (40 * 6))
        x = 1
        cycle = 0
        for line in data:
            line = line.split(" ")
            crt = self.draw(crt, cycle, x)
            if line[0] == "addx":
                cycle += 1
                crt = self.draw(crt, cycle, x)
                x += int(line[1])
            cycle += 1

        for limit in range(6):
            print("".join(crt[limit * 40 : (limit + 1) * 40]))

        lit = 0
        for pixel in crt:
            if pixel == "■":
                lit += 1

        return lit


day = Day()
