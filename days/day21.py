from advent_day import AdventDay
from sympy import solve


class Day(AdventDay):
    test_files = {"data/day21/example.txt": [152, 301]}
    data_file = "data/day21/data.txt"

    operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        variables = {}
        for i, line in enumerate(data):
            variable, equation = line.split(": ")
            variables[variable] = equation

        for variable, equation in variables.items():
            equation = equation.split(" ")
            if len(equation) == 3:
                variables[variable] = {
                    "left": equation[0],
                    "op": equation[1],
                    "right": equation[2],
                }
            else:
                variables[variable] = int(equation[0])
        return variables

    def calculate(self, variables, variable="root", humn=None):
        if humn is not None:
            variables["humn"] = humn
        formula = variables[variable]
        if type(formula) is int:
            return formula
        else:
            left = self.calculate(variables, formula["left"])
            right = self.calculate(variables, formula["right"])
            return self.operations[formula["op"]](left, right)

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def simplify(self, variables, variable="root"):
        if variable in variables:
            formula = variables[variable]
        else:
            return variable
        if type(formula) is int:
            return str(formula)
        else:
            left = str(self.simplify(variables, formula["left"]))
            op = formula["op"]
            right = str(self.simplify(variables, formula["right"]))

            if self.is_number(left) and self.is_number(right):
                return eval(f"({left} {op} {right})")

            return f"({str(left)} {op} {str(right)})"

    def part_1_logic(self, variables):
        root_result = self.calculate(variables)
        return int(root_result)

    def part_2_logic(self, variables):
        variables["root"]["op"] = "-"
        del variables["humn"]
        simple = self.simplify(variables)
        results = solve(simple)
        return int(results[0])


day = Day()
