from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day18/example.txt": [64, 58]}
    data_file = "data/day18/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i, line in enumerate(data):
            data[i] = tuple([int(x) for x in line.split(",")])
        return set(data)

    @staticmethod
    def get_neighbours(cube):
        a, b, c = cube
        return [
            (a + 1, b, c),
            (a - 1, b, c),
            (a, b + 1, c),
            (a, b - 1, c),
            (a, b, c + 1),
            (a, b, c - 1),
        ]

    def part_1_logic(self, cubes):
        surface = 0
        for cube in cubes:
            sides = 6
            for neighbour in self.get_neighbours(cube):
                if neighbour in cubes:
                    sides -= 1
            surface += sides
        return surface

    def part_2_logic(self, cubes):
        to_check = [(0, 0, 0)]
        reachable = set()

        xs = [cube[0] for cube in cubes]
        ys = [cube[1] for cube in cubes]
        zs = [cube[2] for cube in cubes]
        min_x = min(xs) - 1
        max_x = max(xs) + 1
        min_y = min(ys) - 1
        max_y = max(ys) + 1
        min_z = min(zs) - 1
        max_z = max(zs) + 1

        while to_check:
            point = to_check.pop()
            for n in self.get_neighbours(point):
                (x, y, z) = n
                if min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z:
                    if n not in cubes and n not in reachable:
                        reachable.add(n)
                        to_check.append(n)

        x_size = max_x - min_x + 1
        y_size = max_y - min_y + 1
        z_size = max_z - min_z + 1
        outside = 2 * (x_size * y_size) + 2 * (y_size * z_size) + 2 * (z_size * x_size)

        return self.part_1_logic(reachable) - outside


day = Day()
