from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day25/example.txt": ["2=-1=0", None]}
    data_file = "data/day25/data.txt"

    translate_map = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        return data

    def from_snafu(self, snafu_num):
        n = 1
        num = 0
        for char in reversed(snafu_num):
            num += n * self.translate_map[char]
            n *= 5
        return num

    @staticmethod
    def to_base_5(num):
        base_5 = ""
        while num:
            base_5 = str(num % 5) + base_5
            num //= 5
        return base_5

    def to_snafu(self, num):
        b5_num = list(reversed(self.to_base_5(num)))

        carry = 0
        for i, digit in enumerate(b5_num):
            digit = int(digit) + carry
            carry = digit // 5
            digit = digit % 5
            if digit in {3, 4}:
                b5_num[i] = "-" if digit == 4 else "="
                carry += 1
            else:
                b5_num[i] = str(digit)

        snafu_num = "".join(list(reversed(b5_num)))
        if carry:
            snafu_num = str(carry) + snafu_num
        return snafu_num

    def part_1_logic(self, data):
        summa = sum([self.from_snafu(snafu_num) for snafu_num in data])
        return self.to_snafu(summa)


day = Day()
