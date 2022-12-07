import re

from advent_day import AdventDay


def chunk(lst, chunk_size=4):
    list_chunked = [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]
    return list_chunked


class Day(AdventDay):
    test_files = {"data/day5/example.txt": ["CMZ", "MCD"]}
    data_file = "data/day5/data.txt"

    def parse_file(self, data):
        crates_r = re.compile("\[(\w)]| {4}")
        moves_r = re.compile("move (\d+) from (\d) to (\d)")

        data = data.split("\n")
        rows = []
        columns = []
        commands = []
        for line in data[:-1]:
            if crates_r.match(line):
                rows.append(re.findall(crates_r, line))
            elif moves_r.match(line):
                c_num, c_from, c_to = re.findall(moves_r, line)[0]
                commands.append((int(c_num), int(c_from), int(c_to)))

        for _ in range(len(rows[-1])):
            columns.append([])

        for row in reversed(rows):
            for i in range(len(row)):
                if row[i]:
                    columns[i].append(row[i])

        return columns, commands

    def part_1_logic(self, data):
        columns, commands = data
        for command in commands:
            q, f, t = command
            for i in range(q):
                columns[t - 1].append(columns[f - 1].pop())

        end_crates = ""
        for column in columns:
            end_crates += column[-1]
        return end_crates

    def part_2_logic(self, data):
        columns, commands = data
        for command in commands:
            q, f, t = command
            buffer = []
            for i in range(q):
                buffer.append(columns[f - 1].pop())
            columns[t - 1] += reversed(buffer)

        end_crates = ""
        for column in columns:
            end_crates += column[-1]
        return end_crates


day = Day()
