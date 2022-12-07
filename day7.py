import re
from collections import defaultdict
from copy import copy

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day7/example.txt": [95437, 24933642]}
    data_file = "data/day7/data.txt"

    def parse_file(self, data):
        return data.split("\n")[:-1]

    @staticmethod
    def up(path, _, sizes):
        return path[:-1], sizes

    @staticmethod
    def down(path, cmd, sizes):
        directory = cmd.split(" ")[2]
        if directory == "/":
            directory = "~"
        path.append(directory)
        return path, sizes

    @staticmethod
    def file(path, cmd, sizes):
        cmd = cmd.split(" ")
        temp_path = copy(path)
        for i in range(len(temp_path)):
            sizes["/".join(temp_path)] += int(cmd[0])
            temp_path.pop()
        return path, sizes

    def get_sizes(self, data):

        cmd_rs = {
            r"\$ cd \.\.": self.up,  # $ cd ..
            r"\$ cd (\w|\/)": self.down,  # $ cd folder
            r"[0-9]+ .+": self.file,  # 123 e.txt
        }

        path = []
        sizes = defaultdict(int)

        for cmd in data:
            for cmd_r, func in cmd_rs.items():
                if re.match(cmd_r, cmd):
                    path, sizes = func(path, cmd, sizes)

        return sizes

    def part_1_logic(self, data):
        sizes = self.get_sizes(data)
        to_delete_size = 0
        for dir_name, size in sizes.items():
            if size <= 100000:
                to_delete_size += size
        return to_delete_size

    def part_2_logic(self, data):
        sizes = self.get_sizes(data)
        space_available = 70000000 - sizes["~"]
        space_needed = 30000000
        to_delete_size = space_needed - space_available
        for size in sorted(list(sizes.values())):
            if size >= to_delete_size:
                return size


day = Day()
