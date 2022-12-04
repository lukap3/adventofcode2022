from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day4/example.txt": [2, 4]}
    data_file = "data/day4/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            d = data[i].split(",")
            d[0] = [int(a) for a in d[0].split("-")]
            d[1] = [int(a) for a in d[1].split("-")]
            data[i] = (d[0], d[1])
        return data

    @staticmethod
    def includes(s1, s2):
        return s1[0] >= s2[0] and s1[1] <= s2[1]

    @staticmethod
    def overlaps(s1, s2):
        return s1[0] <= s2[1] and s2[0] <= s1[1]

    def part_1_logic(self, data):
        count = 0
        for pair in data:
            e1, e2 = pair
            if self.includes(e1, e2) or self.includes(e2, e1):
                count += 1
        return count

    def part_2_logic(self, data):
        count = 0
        for pair in data:
            e1, e2 = pair
            if self.overlaps(e1, e2) or self.overlaps(e2, e1):
                count += 1
        return count


day = Day()
