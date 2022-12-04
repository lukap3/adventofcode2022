from copy import deepcopy
from typing import Any, Dict, List


def color(text, cl):
    colors = {"green": "\033[92m", "red": "\033[91m"}
    return colors[cl] + text + "\033[0m"


class AdventDay:
    test_files: Dict[str, List] = {}
    data_file: str = ""

    def __init__(self):
        self.test_data = [self.read_file(test_file) for test_file in self.test_files]
        self.test_data = []
        self.test_solutions = []
        for test_file, test_solution in self.test_files.items():
            self.test_data.append(self.read_file(test_file))
            self.test_solutions.append(test_solution)
        self.data = self.read_file(self.data_file)
        self.run()

    def read_file(self, file: str) -> str:
        file_data = open(file, "r").read()
        return self.parse_file(file_data)

    def parse_file(self, file_data: str) -> Any:
        return file_data.split(",")

    def part_1_logic(self, data: Any) -> Any:
        return None

    def part_2_logic(self, data: Any) -> Any:
        return None

    def run(self) -> Any:
        if self.run_tests():
            result = self.part_1_logic(deepcopy(self.data))
            print(f"PART 1 RESULT: {result}")
            result = self.part_2_logic(deepcopy(self.data))
            print(f"PART 2 RESULT: {result}")

    def run_tests(self) -> Any:
        print("----- Running tests -----")
        count = 0
        for i, data in enumerate(self.test_data):
            test_result = self.part_1_logic(deepcopy(data))
            if test_result == self.test_solutions[i][0]:
                print(f"PART 1 TEST {i+1}: {test_result}", color("SUCCESS", "green"))
                count += 1
            else:
                print(
                    f"PART 1 TEST {i+1}: {test_result}",
                    color("FAILED", "red"),
                    f"(expected {self.test_solutions[i][0]})",
                )
            test_result = self.part_2_logic(deepcopy(data))
            if test_result == self.test_solutions[i][1]:
                print(f"PART 2 TEST {i+1}: {test_result}", color("SUCCESS", "green"))
                count += 1
            else:
                print(
                    f"PART 2 TEST {i+1}: {test_result}",
                    color("FAILED", "red"),
                    f"(expected {self.test_solutions[i][1]})",
                )

        print("-------------------------")
        print(f"{count}/{len(self.test_data) * 2} tests succeeded")
        print("-------------------------")

        return count == len(self.test_data) * 2
