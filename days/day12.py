from advent_day import AdventDay
from dijkstar import Graph, NoPathError, find_path


class Day(AdventDay):
    test_files = {"data/day12/example.txt": [31, 29]}
    data_file = "data/day12/data.txt"

    def parse_file(self, data):
        return data.split("\n")[:-1]

    @staticmethod
    def get_ord(char):
        if char == "S":
            return ord("a")
        elif char == "E":
            return ord("z")
        else:
            return ord(char)

    def get_neighbours(self, data, x, y):
        n_coords = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        viable = []
        s_ord = self.get_ord(data[x][y])
        for nx, ny in n_coords:
            if 0 <= nx < len(data) and 0 <= ny < len(data[nx]):
                n_ord = self.get_ord(data[nx][ny])
                if (n_ord - s_ord) <= 1:
                    viable.append((nx, ny))
        return viable

    def build_graph(self, data):
        graph = Graph()
        for x in range(len(data)):
            for y in range(len(data[x])):
                neighbours = self.get_neighbours(data, x, y)
                for neighbour in neighbours:
                    graph.add_edge((x, y), neighbour, 1)
        return graph

    def part_1_logic(self, data):
        start = None
        end = None
        graph = self.build_graph(data)
        for x in range(len(data)):
            for y in range(len(data[x])):
                if data[x][y] == "S":
                    start = (x, y)
                elif data[x][y] == "E":
                    end = (x, y)

        path = find_path(graph, start, end)
        return path.total_cost

    def part_2_logic(self, data):
        distances = []
        graph = self.build_graph(data)
        end = None
        for x in range(len(data)):
            for y in range(len(data[x])):
                if data[x][y] == "E":
                    end = (x, y)
                    break
        for x in range(len(data)):
            for y in range(len(data)):
                if data[x][y] == "a":
                    try:
                        distances.append(find_path(graph, (x, y), end).total_cost)
                    except NoPathError:
                        pass
        return min(distances)


day = Day()
