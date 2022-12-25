from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day24/example.txt": [18, 54]}
    data_file = "data/day24/data.txt"

    clock = ["<", "^", ">", "v"]
    directions = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        blizzards = []
        for i, line in enumerate(data):
            line = []
            for j, char in enumerate(data[i]):
                if char in {"<", ">", "^", "v"}:
                    blizzards.append((i, j, char))
                    line.append(".")
                else:
                    line.append(char)
            data[i] = line
        start = (0, data[0].index("."))
        end = (len(data) - 1, data[-1].index("."))

        return data, blizzards, start, end

    def move_blizzard(self, blizzard, chart):
        direction = self.directions[blizzard[2]]
        pos = (blizzard[0] + direction[0], blizzard[1] + direction[1])
        if chart[pos[0]][pos[1]] == "#":
            return self.teleport_blizzard((pos[0], pos[1], blizzard[2]), chart)

        return pos[0], pos[1], blizzard[2]

    @staticmethod
    def teleport_blizzard(blizzard, chart):
        x, y, direction = blizzard
        if x == len(chart) - 1:
            x = 1
        elif x == 0:
            x = len(chart) - 2
        elif y == len(chart[x]) - 1:
            y = 1
        elif y == 0:
            y = len(chart[x]) - 2
        return x, y, direction

    def move_blizzards(self, blizzards, chart):
        for i, blizzard in enumerate(blizzards):
            blizzards[i] = self.move_blizzard(blizzard, chart)
        return blizzards

    def debug(self, chart, blizzards):
        for i, row in enumerate(chart):
            line = []
            for j, char in enumerate(row):
                blizzards_at = []
                for direction in self.clock:
                    if (i, j, direction) in blizzards:
                        blizzards_at.append(direction)
                if len(blizzards_at) == 0:
                    line.append(char)
                elif len(blizzards_at) == 1:
                    line.append(blizzards_at[0])
                else:
                    line.append(str(len(blizzards_at)))
            print("".join(line))

    @staticmethod
    def get_next_states(position, chart, blizzards):
        moves = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        x, y = position
        blizzard_positions = {(blizzard[0], blizzard[1]) for blizzard in blizzards}
        next_states = set()
        for (mx, my) in moves:
            new_x, new_y = x + mx, y + my
            if 0 <= new_x < len(chart) and 0 <= new_y < len(chart[new_x]):
                if (new_x, new_y) not in blizzard_positions and chart[new_x][
                    new_y
                ] != "#":
                    next_states.add((new_x, new_y))
        return next_states

    def bfs(self, chart, blizzards, start, end):
        states = {start}
        depth = 0
        while True:
            blizzards = self.move_blizzards(blizzards, chart)
            all_next_states = set()
            for state in states:
                all_next_states.update(self.get_next_states(state, chart, blizzards))
            states = all_next_states
            depth += 1
            if end in states:
                return depth

    def part_1_logic(self, data):
        chart, blizzards, start, end = data
        depth = self.bfs(chart, blizzards, start, end)

        return depth

    def part_2_logic(self, data):
        chart, blizzards, start, end = data
        depth_1 = self.bfs(chart, blizzards, start, end)
        depth_2 = self.bfs(chart, blizzards, end, start)
        depth_3 = self.bfs(chart, blizzards, start, end)

        return depth_1 + depth_2 + depth_3


day = Day()
