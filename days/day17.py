from copy import deepcopy

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day17/example.txt": [3068, 1514285714288]}
    data_file = "data/day17/data.txt"

    rocks = [
        (1, [(0, 2), (0, 3), (0, 4), (0, 5)]),
        (3, [(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)]),
        (3, [(0, 4), (1, 4), (2, 2), (2, 3), (2, 4)]),
        (4, [(0, 2), (1, 2), (2, 2), (3, 2)]),
        (2, [(0, 2), (0, 3), (1, 2), (1, 3)]),
    ]

    def parse_file(self, data):
        data = data.split("\n")
        return list(data[0])

    @staticmethod
    def fill_board(board):
        highest_rock = 0
        for i, line in enumerate(board):
            if "#" in line:
                highest_rock = i
                break
        if highest_rock < 3:
            for _ in range(3 - highest_rock):
                board = [list("       ")] + board
        return board

    # returns a new board (added rows)
    # and a list of indexes of rock "particles"
    def add_rock(self, board, idx):
        board = self.fill_board(board)
        rock_idx = idx % len(self.rocks)
        add_rows, rock_parts = self.rocks[rock_idx]
        board = [list("       ") for _ in range(add_rows)] + board
        return board, rock_parts

    @staticmethod
    def drop_rock_once(board, rock_parts):
        for i, (rock_i, rock_j) in enumerate(rock_parts):
            try:
                if board[rock_i + 1][rock_j] != " ":
                    return False
            except IndexError:
                return False
        return True

    @staticmethod
    def shift_rock_once(board, rock_parts, direction):
        rock_parts_c = deepcopy(rock_parts)
        if direction == "<":
            move = -1
        else:
            move = 1
        for i, (a, b) in enumerate(rock_parts_c):
            rock_parts_c[i] = (a, b + move)
            try:
                if board[a][b + move] == "#" or (b + move < 0):
                    return rock_parts
            except IndexError:
                return rock_parts
        return rock_parts_c

    def drop_rock(self, board, rock_parts, jet_pattern):
        while True:
            direction = jet_pattern[0]
            rock_parts = self.shift_rock_once(board, rock_parts, direction)
            jet_pattern = jet_pattern[1:] + [direction]
            dropped = self.drop_rock_once(board, rock_parts)
            if dropped and "#" not in board[0]:
                board = board[1:]
            elif dropped:
                for i in range(len(rock_parts)):
                    rock_parts[i] = (rock_parts[i][0] + 1, rock_parts[i][1])
            else:
                break
        for rock_i, rock_j in rock_parts:
            board[rock_i][rock_j] = "#"
        return board, jet_pattern

    @staticmethod
    def debug(board, rock_parts=None):
        if rock_parts is None:
            rock_parts = []
        c_board = deepcopy(board)
        for i in range(len(c_board)):
            for j in range(len(c_board[i])):
                if (i, j) in rock_parts:
                    c_board[i][j] = "@"
        for row in c_board:
            print("|" + "".join(row).replace(" ", ".") + "|")
        print("+-------+")

    def simplify_board(self, board):
        for i in range(len(board) - 1):
            row1 = board[i]
            row2 = board[i + 1]
            row_sum = 0
            for j in range(len(row1)):
                row_sum += 1 if row1[j] == "#" or row2[j] == "#" else 0
            if row_sum == 7:
                return board[:i], len(board[i:])
        return board, 0

    def part_1_logic(self, jet_pattern):
        board = []
        for x in range(2022):
            board, rock_parts = self.add_rock(board, x)
            board, jet_pattern = self.drop_rock(board, rock_parts, jet_pattern)

        return len(board)

    def part_2_logic(self, jet_pattern):
        board = []
        height = 0
        cycles = {}
        num_rocks = 1000000000000
        repeating_cycle = None
        for x in range(num_rocks):
            board, rock_parts = self.add_rock(board, x)
            board, jet_pattern = self.drop_rock(board, rock_parts, jet_pattern)
            board, cycle_height = self.simplify_board(board)
            if cycle_height:
                height += cycle_height
                cycle = (cycle_height, x % len(self.rocks), hash("".join(jet_pattern)))
                if cycle in cycles:
                    cycles[cycle].append((x, cycle_height, height))
                    repeating_cycle = cycle
                    break
                else:
                    cycles[cycle] = [(x, height, height)]

        cs = cycles[repeating_cycle]

        a_step = cs[1][0] - cs[0][0]
        c_step = cs[1][2] - cs[0][2]
        m = int((num_rocks - cs[0][0]) / a_step)
        simulated_cs = list(cs[0])
        simulated_cs[0] += m * a_step
        simulated_cs[2] += m * c_step
        height = simulated_cs[2]

        board = []
        for x in range(simulated_cs[0] + 1, 1000000000000):
            board, rock_parts = self.add_rock(board, x)
            board, jet_pattern = self.drop_rock(board, rock_parts, jet_pattern)

        return height + len(board)


day = Day()
