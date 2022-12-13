import functools

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day13/example.txt": [13, 140]}
    data_file = "data/day13/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        packet_pairs = [[]]
        for i, line in enumerate(data):
            if line == "":
                packet_pairs.append([])
            else:
                packet = eval(line)
                packet_pairs[-1].append(packet)
        return packet_pairs

    @classmethod
    def compare(cls, left, right, d=0):
        if type(left) is int and type(right) is int:
            return left - right
        elif type(left) is list and type(right) is list:
            for i in range(len(right)):
                try:
                    res = cls.compare(left[i], right[i], d + 1)
                except IndexError:
                    return -1
                if res != 0:
                    return res
            if len(right) == len(left):
                return 0
            return 1
        elif type(left) is list and type(right) is int:
            return cls.compare(left, [right], d + 1)
        elif type(left) is int and type(right) is list:
            return cls.compare([left], right, d + 1)

    def part_1_logic(self, packet_pairs):
        idx_sum = 0
        for i, (left, right) in enumerate(packet_pairs):
            res = self.compare(left, right, 0)
            if res < 0:
                idx_sum += i + 1
        return idx_sum

    def part_2_logic(self, packet_pairs):
        additional_packets = [[[2]], [[6]]]
        packets = [
            packet for pair in packet_pairs for packet in pair
        ] + additional_packets
        packets.sort(key=functools.cmp_to_key(self.compare))
        m = 1
        for packet in additional_packets:
            m *= packets.index(packet) + 1
        return m


day = Day()
