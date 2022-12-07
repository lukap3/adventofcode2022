from copy import copy

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day7/example.txt": [95437, 24933642]}
    data_file = "data/day7/data.txt"

    def parse_file(self, data):
        return data.split("\n")[:-1]

    @staticmethod
    def get_sizes(data):
        current_path = []
        sizes = {}
        for cmd in data:
            cmd = cmd.split(" ")
            if cmd[0] == "$":
                if cmd[1] == "cd" and cmd[2] == "..":
                    current_path.pop()
                elif cmd[1] == "cd":
                    if cmd[2] == "/":
                        cmd[2] = "~"
                    current_path.append(cmd[2])
                elif cmd[1] == "ls":
                    pass
            else:
                if cmd[0] != "dir":
                    size = int(cmd[0])
                    temp_path = copy(current_path)
                    for i in range(len(temp_path)):
                        path = "/".join(temp_path)
                        if path in sizes:
                            sizes[path] += size
                        else:
                            sizes[path] = size
                        temp_path.pop()
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
