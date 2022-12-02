from advent_day import AdventDay


class Day(AdventDay):
    test_files = {
        "data/day1/example.txt": [24000, 45000],
    }
    data_file = "data/day1/data.txt"

    def parse_file(self, data):
        return data.split("\n")

    @staticmethod
    def get_sums(data):
        elves = [[]]
        idx = 0
        for line in data:
            if line == "":
                idx += 1
                elves.append([])
            else:
                elves[idx].append(int(line))
        sums = []
        for elf in elves:
            sums.append(sum(elf))
        return sums

    def part_1_logic(self, data):
        sums = self.get_sums(data)
        return max(sums)

    def part_2_logic(self, data):
        sums = self.get_sums(data)
        return sum(sorted(sums, reverse=True)[0:3])


day = Day()
