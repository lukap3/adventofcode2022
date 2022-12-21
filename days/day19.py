import re
from copy import deepcopy
from threading import Thread

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day19/example.txt": [33, 3472]}
    data_file = "data/day19/data.txt"

    @staticmethod
    def parse_materials(materials):
        materials = materials[0]
        cost = {}
        for i in range(0, len(materials), 2):
            cost[materials[i + 1]] = int(materials[i])
        return cost

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        blueprints = []
        for line in data:
            ore_robot = re.findall("ore robot costs (\d+) (\w+)", line)
            clay_robot = re.findall("clay robot costs (\d+) (\w+)", line)
            obsidian_robot = re.findall(
                "obsidian robot costs (\d+) (\w+) and (\d+) (\w+)", line
            )
            geode_robot = re.findall(
                "geode robot costs (\d+) (\w+) and (\d+) (\w+)", line
            )
            blueprints.append(
                {
                    "ore": self.parse_materials(ore_robot),
                    "clay": self.parse_materials(clay_robot),
                    "obsidian": self.parse_materials(obsidian_robot),
                    "geode": self.parse_materials(geode_robot),
                }
            )
        return blueprints

    @staticmethod
    def get_build_options(state, blueprint):
        options = [None]
        for robot_type, costs in blueprint.items():
            can_build = True
            if state["robots"][robot_type] < state["robot_limits"][robot_type]:
                for material_type, amount in costs.items():
                    if state["materials"][material_type] < amount:
                        can_build = False
                if can_build:
                    options.append(robot_type)
        return options

    @staticmethod
    def build_state(state, blueprint, robot_type):
        state = deepcopy(state)
        if robot_type is None:
            return state

        costs = blueprint[robot_type]
        for material, amount in costs.items():
            state["materials"][material] -= amount
        state["building"] = robot_type
        return state

    @staticmethod
    def collect_state(state):
        for robot_type, amount in state["robots"].items():
            state["materials"][robot_type] += amount
        return state

    @staticmethod
    def complete_building(state):
        if state["building"] is not None:
            state["robots"][state["building"]] += 1
            state["building"] = None
        return state

    def get_next_states(self, state, blueprint):
        build_options = self.get_build_options(state, blueprint)
        states = []
        for option in build_options:
            states.append(self.build_state(state, blueprint, option))

        for state in states:
            self.collect_state(state)

        for state in states:
            self.complete_building(state)

        for state in states:
            state["minutes"] -= 1

        return states

    @staticmethod
    def remove_duplicates(states):
        state_map = {}
        for state in states:
            state_map[
                (
                    state["materials"]["ore"],
                    state["materials"]["clay"],
                    state["materials"]["obsidian"],
                    state["materials"]["geode"],
                    state["robots"]["ore"],
                    state["robots"]["clay"],
                    state["robots"]["obsidian"],
                    state["robots"]["geode"],
                )
            ] = state
        return list(state_map.values())

    def prune_states(self, states):
        # TODO only keep the states with the best "potential"
        return self.remove_duplicates(states)

    @staticmethod
    def init_state(blueprint, t):
        state = {
            "materials": {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0},
            "robots": {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0},
            "robot_limits": {"ore": 0, "clay": 0, "obsidian": 0, "geode": 100000},
            "minutes": t,
            "building": None,
        }
        for robot_type, costs in blueprint.items():
            for material, amount in costs.items():
                if amount > state["robot_limits"][material]:
                    state["robot_limits"][material] = amount
        return state

    def test_blueprint(self, blueprint, index, results, t=24):
        state = self.init_state(blueprint, t)
        states = [deepcopy(state)]
        for i in range(t):
            next_states = []
            for state in self.prune_states(states):
                next_states += self.get_next_states(state, blueprint)
            states = next_states

        geodes = []
        for state in states:
            geodes.append(state["materials"]["geode"])
        results[str(index)] = max(geodes)

    def part_1_logic(self, blueprints):
        threads = []
        results = {}
        for i, blueprint in enumerate(blueprints):
            t = Thread(target=self.test_blueprint, args=(blueprint, i + 1, results))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        summa = 0
        for index, value in results.items():
            summa += int(index) * value
        return summa

    def part_2_logic(self, blueprints):
        threads = []
        results = {}
        for i, blueprint in enumerate(blueprints[:3]):
            t = Thread(target=self.test_blueprint, args=(blueprint, i + 1, results, 32))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        summa = 1
        for index, value in results.items():
            summa *= value
        return summa


day = Day()
