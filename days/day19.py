import re
from threading import Thread

from advent_day import AdventDay


class Blueprint:
    def __init__(self, input_string):
        vals = [int(i) for i in re.findall(r"\d+", input_string)]
        self.id = vals[0]
        self.cost = {
            "ore": {"ore": vals[1]},
            "clay": {"ore": vals[2]},
            "obsidian": {"ore": vals[3], "clay": vals[4]},
            "geode": {"ore": vals[5], "obsidian": vals[6]},
        }
        self.useful = {
            "ore": max(
                self.cost["clay"]["ore"],
                self.cost["obsidian"]["ore"],
                self.cost["geode"]["ore"],
            ),
            "clay": self.cost["obsidian"]["clay"],
            "obsidian": self.cost["geode"]["obsidian"],
            "geode": float("inf"),
        }


class State:
    def __init__(self, robots=None, resources=None, ignored=None):
        self.robots = (
            robots.copy()
            if robots
            else {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        )
        self.resources = (
            resources.copy()
            if resources
            else {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        )
        self.ignored = ignored.copy() if ignored else []

    def copy(self):
        return State(self.robots, self.resources, self.ignored)

    def __gt__(self, other):
        return self.resources["geode"] > other.resources["geode"]

    def __repr__(self):
        return f"{{robots: {self.robots}, resources: {self.resources}}}"


def get_daily_input():
    file_data = open("data/day19/data.txt", "r").read()
    return file_data.split("\n")[:-1]


class Day(AdventDay):
    test_files = {"data/day19/example.txt": [33, 3472]}
    data_file = "data/day19/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        blueprints = []
        for i, line in enumerate(data):
            blueprints.append(Blueprint(line))
        return blueprints

    def dfs(self, blueprint, prior_states, timelimit):
        time_remaining = timelimit - len(prior_states)
        curr_state = prior_states[-1]

        options: list[str] = []
        if time_remaining >= 0:
            for robot, cost in blueprint.cost.items():
                if (
                    curr_state.robots[robot] < blueprint.useful[robot]
                    and all(curr_state.resources[k] >= v for k, v in cost.items())
                    and robot not in curr_state.ignored
                ):
                    options.append(robot)

            if "geode" in options:
                options = ["geode"]
            elif time_remaining < 1:
                options = []
            else:
                if (
                    curr_state.robots["clay"] > 3
                    or curr_state.robots["obsidian"]
                    or "obsidian" in options
                ) and "ore" in options:
                    options.remove("ore")
                if (
                    curr_state.robots["obsidian"] > 3
                    or curr_state.robots["geode"]
                    or "geode" in options
                ) and "clay" in options:
                    options.remove("clay")

            next_state = curr_state.copy()
            for r, n in next_state.robots.items():
                next_state.resources[r] += n

            next_state.ignored += options
            results = [self.dfs(blueprint, prior_states + [next_state], timelimit)]

            for opt in options:
                next_state_opt = next_state.copy()
                next_state_opt.ignored = []
                next_state_opt.robots[opt] += 1
                for r, n in blueprint.cost[opt].items():
                    next_state_opt.resources[r] -= n
                results.append(
                    self.dfs(blueprint, prior_states + [next_state_opt], timelimit)
                )

            return max(results)

        return prior_states[-1].resources["geode"], prior_states

    def evaluate_blueprint(self, blueprint, results, timelimit=24):
        r = self.dfs(blueprint, [State()], timelimit)
        results[blueprint.id] = r[0]

    def part_1_logic(self, blueprints):
        results = {}
        threads = []
        for blueprint in blueprints:
            thread = Thread(target=self.evaluate_blueprint, args=(blueprint, results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        summa = 0
        for index, result in results.items():
            summa += index * result

        return summa

    def part_2_logic(self, blueprints):
        results = {}
        threads = []
        for blueprint in blueprints[:3]:
            thread = Thread(
                target=self.evaluate_blueprint, args=(blueprint, results, 32)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        summa = 1
        for _, result in results.items():
            summa *= result

        return summa


day = Day()
