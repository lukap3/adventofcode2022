from advent_day import AdventDay


class Day2(AdventDay):
    test_files = {
        "data/day2/example.txt": [15, 12],
    }
    data_file = "data/day2/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = data[i].split(" ")
        return data

    @staticmethod
    def get_points(p1, p2):
        base_points = 1 + ["A", "B", "C"].index(p2)
        beats = {"B": "A", "C": "B", "A": "C"}
        if beats[p2] == p1:
            return 6 + base_points
        elif beats[p1] == p2:
            return base_points
        else:
            return 3 + base_points

    @staticmethod
    def generate_hand(p1, p2):
        idx = ["X", "Y", "Z"].index(p2)
        gens = {"A": ["C", "A", "B"], "B": ["A", "B", "C"], "C": ["B", "C", "A"]}
        return gens[p1][idx]

    def part_1_logic(self, data):
        points = 0
        for p1, p2 in data:
            p2 = p2.replace("X", "A").replace("Y", "B").replace("Z", "C")
            points += self.get_points(p1, p2)
        return points

    def part_2_logic(self, data):
        points = 0
        for p1, p2 in data:
            h2 = self.generate_hand(p1, p2)
            points += self.get_points(p1, h2)
        return points


day = Day2()
