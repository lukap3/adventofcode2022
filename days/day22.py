import re
from typing import Callable

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day22/example.txt": [6032, 5031]}
    data_file = "data/day22/data.txt"

    clock = ["R", "D", "L", "U"]
    directions = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

    quadrants: dict[tuple, list] = {}
    quadrants_by_id: dict[int, tuple] = {}
    q_size: int = 0
    visited: list[tuple] = []
    teleport_rules: dict[tuple, tuple] = {}
    d_lambdas: dict[tuple, Callable] = {}

    def get_d_lambdas(self):
        max_q = self.q_size - 1
        return {
            ("R", "R"): lambda x, y: (x, 0),
            ("R", "D"): lambda x, y: (0, max_q - x),
            ("R", "L"): lambda x, y: (max_q - x, max_q),
            ("R", "U"): lambda x, y: (max_q, x),
            ("D", "R"): lambda x, y: (max_q - y, 0),
            ("D", "D"): lambda x, y: (0, y),
            ("D", "L"): lambda x, y: (y, max_q),
            ("D", "U"): lambda x, y: (max_q, max_q - y),
            ("L", "R"): lambda x, y: (max_q - x, 0),
            ("L", "D"): lambda x, y: (0, x),
            ("L", "L"): lambda x, y: (x, max_q),
            ("L", "U"): lambda x, y: (max_q, max_q - x),
            ("U", "R"): lambda x, y: (y, 0),
            ("U", "D"): lambda x, y: (0, max_q - y),
            ("U", "L"): lambda x, y: (max_q - y, max_q),
            ("U", "U"): lambda x, y: (max_q, y),
        }

    def get_teleport_rule(self, quadrant_id, direction):
        target_quadrant, target_direction = self.teleport_rules[
            (quadrant_id, direction)
        ]
        d_lambda = self.d_lambdas[(direction, target_direction)]
        return target_quadrant, target_direction, d_lambda

    @staticmethod
    def generate_teleport_rules(rule_type):
        if rule_type == 4:
            return {
                (1, "R"): (6, "L"),
                (1, "D"): (4, "D"),
                (1, "L"): (3, "D"),
                (1, "U"): (2, "D"),
                (2, "R"): (3, "R"),
                (2, "D"): (5, "U"),
                (2, "L"): (6, "U"),
                (2, "U"): (1, "D"),
                (3, "R"): (4, "R"),
                (3, "D"): (5, "R"),
                (3, "L"): (2, "L"),
                (3, "U"): (1, "R"),
                (4, "R"): (6, "D"),
                (4, "D"): (5, "D"),
                (4, "L"): (3, "L"),
                (4, "U"): (1, "U"),
                (5, "R"): (6, "R"),
                (5, "D"): (2, "U"),
                (5, "L"): (3, "U"),
                (5, "U"): (4, "U"),
                (6, "R"): (1, "L"),
                (6, "D"): (2, "R"),
                (6, "L"): (5, "L"),
                (6, "U"): (4, "L"),
            }
        else:
            return {
                (1, "R"): (2, "R"),
                (1, "D"): (3, "D"),
                (1, "L"): (4, "R"),
                (1, "U"): (6, "R"),
                (2, "R"): (5, "L"),
                (2, "D"): (3, "L"),
                (2, "L"): (1, "L"),
                (2, "U"): (6, "U"),
                (3, "R"): (2, "U"),
                (3, "D"): (5, "D"),
                (3, "L"): (4, "D"),
                (3, "U"): (1, "U"),
                (4, "R"): (5, "R"),
                (4, "D"): (6, "D"),
                (4, "L"): (1, "R"),
                (4, "U"): (3, "R"),
                (5, "R"): (2, "L"),
                (5, "D"): (6, "L"),
                (5, "L"): (4, "L"),
                (5, "U"): (3, "U"),
                (6, "R"): (5, "U"),
                (6, "D"): (2, "D"),
                (6, "L"): (1, "D"),
                (6, "U"): (4, "U"),
            }

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        instructions = data[-1]
        instructions = re.findall("(\d+)|(\w)", instructions)
        for i, instr in enumerate(instructions):
            if instr[0]:
                instructions[i] = int(instr[0])
            else:
                instructions[i] = instr[1]

        data = data[:-2]
        chart = []
        for i, line in enumerate(data):
            chart.append(list(line))
        return chart, instructions

    @staticmethod
    def get_start(chart):
        start_x = 0
        start_y = 0
        for i in range(len(chart[0])):
            if chart[0][i] == ".":
                start_y = i
                break
        return start_x, start_y

    def teleport(self, chart, pos, direction):
        original_pos = pos
        temp_poss = {
            "R": (pos[0], 0),
            "L": (pos[0], len(chart[pos[0]]) - 1),
            "D": (0, pos[1]),
            "U": (len(chart) - 1, pos[1]),
        }
        pos = temp_poss[direction]

        # fix position
        while True:
            d = self.directions[direction]
            try:
                _ = chart[pos[0]][pos[1]]
                break
            except IndexError:
                new_x = pos[0] + d[0]
                new_y = pos[1] + d[1]
                pos = (new_x, new_y)

        if chart[pos[0]][pos[1]] == "#":
            return original_pos

        d = self.directions[direction]
        while chart[pos[0]][pos[1]] != ".":
            pos = pos[0] + d[0], pos[1] + d[1]
            if chart[pos[0]][pos[1]] == "#":
                return original_pos
        return pos

    def move(self, chart, pos, direction, steps):
        d = self.directions[direction]
        for _ in range(steps):
            new_x = pos[0] + d[0]
            new_y = pos[1] + d[1]

            if (
                new_x >= len(chart)
                or new_y >= len(chart[new_x])
                or new_x < 0
                or new_y < 0
                or chart[new_x][new_y] == " "
            ):
                new_x, new_y = self.teleport(chart, pos, direction)

            if chart[new_x][new_y] == "#":
                break
            pos = (new_x, new_y)
            self.visited.append(pos)

        return pos

    def turn(self, direction, clockwise):
        current_index = self.clock.index(direction)
        if clockwise:
            new_index = current_index + 1
        else:
            new_index = current_index - 1
        return self.clock[new_index % 4]

    def debug(self, chart):
        for i in range(len(chart)):
            for j in range(len(chart[i])):
                if (i, j) in self.visited:
                    chart[i][j] = "█"
        for line in chart:
            print("".join(line))

    def part_1_logic(self, data):
        chart, instructions = data

        direction = "R"
        pos = self.get_start(chart)

        self.visited = []

        for instr in instructions:
            if type(instr) is int:
                pos = self.move(chart, pos, direction, instr)
            else:
                direction = self.turn(direction, instr == "R")

        final_row = pos[0] + 1
        final_col = pos[1] + 1
        direction_index = self.clock.index(direction)

        return (1000 * final_row) + (4 * final_col) + direction_index

    @staticmethod
    def get_quadrant_size(chart):
        min_width = len(chart[0])
        for line in chart:
            width = len("".join(line).strip())
            if width < min_width:
                min_width = width
        return min_width

    def get_quadrants(self, chart):
        size = self.get_quadrant_size(chart)
        quadrants = {}
        quadrant_num = 1
        quadrants_by_numbers = {}
        for i in range(5):
            for j in range(5):
                quadrant = []
                for line in chart[i * size : (i + 1) * size]:
                    quadrant.append(line[j * size : (j + 1) * size])
                if (
                    quadrant
                    and len(quadrant)
                    and len(quadrant[0]) > 0
                    and quadrant[0][0] != " "
                ):
                    quadrants[(i, j)] = quadrant
                    quadrants_by_numbers[quadrant_num] = (i, j)
                    quadrant_num += 1
        return quadrants, quadrants_by_numbers

    def flatten_cube(self, quadrants, q_size):
        q_poss = {q_pos: q_id for q_id, q_pos in self.quadrants_by_id.items()}
        chart = {}
        for q_pos, quadrant in quadrants.items():
            x, y = q_pos
            q_id = q_poss.get(q_pos, None)
            for i, row in enumerate(quadrant):
                for j, char in enumerate(row):
                    if q_id is not None and (q_id, i, j) in self.visited:
                        chart[(x * q_size + i, (y * q_size + j))] = "█"
                    else:
                        chart[((x * q_size) + i, ((y * q_size) + j))] = char
        return chart

    def debug_cube(self):
        chart = self.flatten_cube(self.quadrants, self.q_size)
        for i in range(self.q_size * 4):
            line = []
            for j in range(self.q_size * 4):
                if (i, j) in chart:
                    line.append(chart[(i, j)])
                else:
                    line.append(" ")
            print("".join(line))

    def teleport_q(self, pos, direction):
        quadrant_id = pos[0]
        new_quadrant_id, new_direction, x_y_func = self.get_teleport_rule(
            quadrant_id, direction
        )
        new_x, new_y = x_y_func(pos[1], pos[2])

        new_quadrant = self.get_current_quadrant((new_quadrant_id, new_x, new_y))
        if new_quadrant[new_x][new_y] == "#":
            return pos, direction
        else:
            return (new_quadrant_id, new_x, new_y), new_direction

    def get_current_quadrant(self, pos):
        quadrant_coordinates = self.quadrants_by_id[pos[0]]
        return self.quadrants[quadrant_coordinates]

    def move_q(self, pos, direction, steps):
        # position = (quadrant, x, y)
        current_quadrant = self.get_current_quadrant(pos)
        for _ in range(steps):
            d = self.directions[direction]
            new_q = pos[0]
            new_x = pos[1] + d[0]
            new_y = pos[2] + d[1]

            if (
                new_x >= len(current_quadrant)
                or new_y >= len(current_quadrant[new_x])
                or new_x < 0
                or new_y < 0
                or current_quadrant[new_x][new_y] == " "
            ):
                new_pos, direction = self.teleport_q(pos, direction)
                new_q = new_pos[0]
                new_x = new_pos[1]
                new_y = new_pos[2]
                current_quadrant = self.get_current_quadrant((new_q, 0, 0))

            if current_quadrant[new_x][new_y] == "#":
                break
            pos = (new_q, new_x, new_y)
            self.visited.append(pos)

        return pos, direction

    def part_2_logic(self, data):
        chart, instructions = data

        self.quadrants, self.quadrants_by_id = self.get_quadrants(chart)
        self.visited = []
        self.q_size = self.get_quadrant_size(chart)
        self.teleport_rules = self.generate_teleport_rules(self.q_size)
        self.d_lambdas = self.get_d_lambdas()

        pos = (1, 0, 0)
        direction = "R"
        for instr in instructions:
            if type(instr) is int:
                pos, direction = self.move_q(pos, direction, instr)
            else:
                direction = self.turn(direction, instr == "R")

        final_position = self.visited[-1]
        direction_index = self.clock.index(direction)

        q_pos = self.quadrants_by_id[final_position[0]]
        final_row = self.q_size * q_pos[0] + final_position[1] + 1
        final_col = self.q_size * q_pos[1] + final_position[2] + 1

        return (1000 * final_row) + (4 * final_col) + direction_index


day = Day()
