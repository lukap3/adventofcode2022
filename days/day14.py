from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day14/example.txt": [24, 93]}
    data_file = "data/day14/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = data[i].split(" -> ")
            data[i] = [d.split(",") for d in data[i]]
            for j, (a, b) in enumerate(data[i]):
                data[i][j] = (int(a), int(b))

        rocks = []
        for rock_cluster in data:
            for i in range(1, len(rock_cluster)):
                prev = rock_cluster[i - 1]
                curr = rock_cluster[i]
                max_x, min_x = max(prev[0], curr[0]), min(prev[0], curr[0])
                for x in range(min_x, max_x + 1):
                    max_y, min_y = max(prev[1], curr[1]), min(prev[1], curr[1])
                    for y in range(min_y, max_y + 1):
                        rocks.append((x, y))

        return set(rocks)

    @staticmethod
    def on_obstacle(rocks, sands, sand):
        below = (sand[0], sand[1] + 1)
        return below in sands or below in rocks

    @staticmethod
    def on_floor(floor, sand):
        below = (sand[0], sand[1] + 1)
        return below[1] == floor

    def sand_fall(self, rocks, sands, sand):
        moved = False
        if not self.on_obstacle(rocks, sands, sand):
            sand[1] += 1
            moved = True
        else:
            dl = (sand[0] - 1, sand[1] + 1)
            dr = (sand[0] + 1, sand[1] + 1)
            if dl not in rocks and dl not in sands:
                sand = list(dl)
                moved = True
            elif dr not in rocks and dr not in sands:
                sand = list(dr)
                moved = True
        return sand, moved

    def part_1_logic(self, rocks):
        sands = set()
        floor = max([rock[1] for rock in rocks]) + 1
        moved = False
        while not moved:
            sand = [500, 0]
            moved = True
            while moved:
                sand, moved = self.sand_fall(rocks, sands, sand)
                if sand[1] == floor:
                    return len(sands)
            if not moved:
                sands.add(tuple(sand))

    def part_2_logic(self, rocks):
        sands = set()
        floor = max([rock[1] for rock in rocks]) + 1
        moved = False
        while not moved:
            sand = [500, 0]
            moved = True
            while moved:
                sand, moved = self.sand_fall(rocks, sands, sand)
                if sand[1] == floor:
                    moved = False
            if not moved:
                sands.add(tuple(sand))
            if sand[1] == 0:
                moved = True

        return len(sands)


day = Day()
