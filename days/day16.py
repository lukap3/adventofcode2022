import re
from copy import copy

import networkx as nx
from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day16/example.txt": [1651, 1707]}
    data_file = "data/day16/data.txt"

    def __init__(self):
        super().__init__()
        self.scores = None

    def parse_file(self, data):
        groups = re.findall(
            r"Valve (\w+) has flow rate=(\d+); .+ valve(?:s\b|\b) (.+)", data
        )
        valves = {}
        for name, flow_rate, connected in groups:
            valves[name] = [int(flow_rate), connected.split(", ")]

        return valves

    @staticmethod
    def generate_graph(valves):
        graph = nx.Graph()
        for valve_name, valve in valves.items():
            for neighbour_valve_name in valve[1]:
                graph.add_edge(valve_name, neighbour_valve_name)
        return graph

    @staticmethod
    def get_all_distances(graph):
        all_shortest = nx.all_pairs_shortest_path(graph)
        distances = {}
        for start_node, target_path in all_shortest:
            distances[start_node] = {}
            for target_node, path in target_path.items():
                if target_node != start_node:
                    distances[start_node][target_node] = len(path) - 1
        return distances

    def bfs(self, current_valve, minutes, flow_rates, distances, rate, score, path):
        if minutes == 0:
            return

        path.append(current_valve)
        rate += flow_rates[current_valve]
        flow_rates[current_valve] = 0
        for next_valve, flow_rate in flow_rates.items():
            if flow_rate > 0:
                distance = distances[current_valve][next_valve]
                if minutes - distance - 1 >= 0:
                    self.bfs(
                        next_valve,
                        minutes - distance - 1,
                        copy(flow_rates),
                        distances,
                        rate,
                        score + ((distance + 1) * rate),
                        copy(path),
                    )
        score += minutes * rate
        self.scores[tuple(path[1:])] = score
        return

    def part_1_logic(self, valves):
        graph = self.generate_graph(valves)
        distances = self.get_all_distances(graph)
        flow_rates = {valve: valve_data[0] for valve, valve_data in valves.items()}

        self.scores = {}
        self.bfs("AA", 30, flow_rates, distances, 0, 0, [])

        return max(self.scores.values())

    def part_2_logic(self, valves):
        graph = self.generate_graph(valves)
        distances = self.get_all_distances(graph)
        flow_rates = {valve: valve_data[0] for valve, valve_data in valves.items()}

        self.scores = {}
        self.bfs("AA", 26, flow_rates, distances, 0, 0, [])

        paths = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        max_double = 0
        for path, score in paths:
            for e_path, e_score in paths:
                if score + e_score <= max_double:
                    break
                if not set(path).intersection(set(e_path)) and path and e_path:
                    max_double = score + e_score

        return max_double


day = Day()
