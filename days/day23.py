from collections import deque

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day23/example.txt": [110, 20]}
    data_file = "data/day23/data.txt"

    def parse_file(self, data):
        elves = set()
        data = [list(line) for line in data.split("\n")[:-1]]
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if char == "#":
                    elves.add((i, j))
        return elves

    @staticmethod
    def get_proposed_move(elf_position, elves, checks):
        er, ec = elf_position
        proposals = []
        for i, check_lambda in enumerate(checks):
            check = check_lambda(er, ec)
            for position in check:
                if position in elves:
                    break
            else:
                proposals.append(check[1])
        if proposals:
            if len(proposals) == 4:
                return None
            return proposals[0]
        return None

    def get_all_proposed_moves(self, elves, checks):
        proposed_moves = {}
        for elf in elves:
            proposed_move = self.get_proposed_move(elf, elves, checks)
            if proposed_move:
                proposed_moves[elf] = proposed_move
        return proposed_moves

    @staticmethod
    def exec_moves(proposed_moves, elves):
        position_counts = {}
        for elf, new_position in proposed_moves.items():
            if new_position:
                if new_position in position_counts:
                    position_counts[new_position] += 1
                else:
                    position_counts[new_position] = 1
        for elf, new_position in proposed_moves.items():
            if position_counts.get(new_position, 2) == 1:
                elves.remove(elf)
                elves.add(new_position)
        return elves

    @staticmethod
    def debug(elves):
        rows = [elf[0] for elf in elves]
        columns = [elf[1] for elf in elves]

        for r in range(min(rows), max(rows) + 1):
            line = []
            for c in range(min(columns), max(columns) + 1):
                if (r, c) in elves:
                    line.append("#")
                else:
                    line.append(".")
            print("".join(line))

    @staticmethod
    def init_checks():
        return deque(
            [
                lambda r, c: [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1)],  # north
                lambda r, c: [(r + 1, c - 1), (r + 1, c), (r + 1, c + 1)],  # south
                lambda r, c: [(r - 1, c - 1), (r, c - 1), (r + 1, c - 1)],  # west
                lambda r, c: [(r - 1, c + 1), (r, c + 1), (r + 1, c + 1)],  # east
            ]
        )

    @staticmethod
    def count_empty(elves):
        rows = [elf[0] for elf in elves]
        columns = [elf[1] for elf in elves]
        return (max(rows) - min(rows) + 1) * (max(columns) - min(columns) + 1) - len(
            elves
        )

    def part_1_logic(self, elves):
        checks = self.init_checks()
        for i in range(10):
            proposed_moves = self.get_all_proposed_moves(elves, checks)
            elves = self.exec_moves(proposed_moves, elves)
            checks.rotate(-1)
        return self.count_empty(elves)

    def part_2_logic(self, elves):
        checks = self.init_checks()
        i = 1
        while True:
            proposed_moves = self.get_all_proposed_moves(elves, checks)
            if not proposed_moves:
                return i
            elves = self.exec_moves(proposed_moves, elves)
            checks.rotate(-1)
            i += 1


day = Day()
