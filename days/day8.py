from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day8/example.txt": [21, 8]}
    data_file = "data/day8/data.txt"

    def parse_file(self, data):
        data = data.split("\n")
        grid = []
        for line in data[:-1]:
            grid.append([int(tree) for tree in line])
        return grid

    @staticmethod
    def get_perspectives(x, y, grid):
        row = grid[x]
        column = [grid[x][y] for x in range(len(grid))]
        return [row[:y][::-1], row[y + 1 :], column[:x][::-1], column[x + 1 :]]

    def is_visible(self, x, y, grid):
        tree_size = grid[x][y]
        perspectives = self.get_perspectives(x, y, grid)
        for p in perspectives:
            if len(p) == 0 or max(p) < tree_size:
                return True
        return False

    def get_scenic_score(self, x, y, grid):
        tree_size = grid[x][y]
        perspectives = self.get_perspectives(x, y, grid)
        score = 1
        for i, p in enumerate(perspectives):
            c = 0
            for tree in p:
                c += 1
                if tree >= tree_size:
                    break
            if c == 0:
                return 0
            score *= c
        return score

    def part_1_logic(self, grid):
        size = len(grid)
        count = (size * 4) - 4
        for x in range(1, size - 1):
            for y in range(1, size - 1):
                if self.is_visible(x, y, grid):
                    count += 1
        return count

    def part_2_logic(self, grid):
        size = len(grid)
        scores = []
        for x in range(1, size - 1):
            for y in range(1, size - 1):
                scores.append(self.get_scenic_score(x, y, grid))
        return max(scores)


day = Day()
