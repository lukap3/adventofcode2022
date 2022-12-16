import re

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"data/day15/example.txt": [26, 56000011]}
    data_file = "data/day15/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        sensors = {}
        m = int(re.findall("(-?\d+)", data[0])[0])
        y = int(re.findall("(-?\d+)", data[1])[0])
        for i in range(2, len(data)):
            numbers = re.findall("(-?\d+)", data[i])
            numbers = [int(n) for n in numbers]
            sensor_x, sensor_y, beacon_x, beacon_y = numbers
            sensors[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
        return sensors, y, m

    @staticmethod
    def get_manhattan(a_coord, b_coord):
        return sum(abs(x - y) for x, y in zip(a_coord, b_coord))

    def add_range(self, ranges, new_range):
        for i, old_range in enumerate(ranges):
            start1, end1 = old_range
            start2, end2 = new_range
            if start1 <= end2 and start2 <= end1:
                min_start = min(start1, start2)
                max_end = max(end1, end2)
                ranges.remove(old_range)
                return self.add_range(ranges, (min_start, max_end))
        ranges.append(new_range)
        return ranges

    def scan_row(self, ranges, row):
        scanned_ranges = []
        for sensor_coord, rng in ranges.items():
            sensor_x, sensor_y = sensor_coord
            if sensor_y > row:
                reach = sensor_y - rng
                overshot = abs(reach - row)
                if row >= reach:
                    a = sensor_x - overshot
                    b = sensor_x + overshot
                    scanned_ranges = self.add_range(scanned_ranges, (a, b + 1))
            else:
                reach = sensor_y + rng
                overshot = abs(reach - row)
                if row <= reach:
                    a = sensor_x - overshot
                    b = sensor_x + overshot
                    scanned_ranges = self.add_range(scanned_ranges, (a, b + 1))
        return scanned_ranges

    def part_1_logic(self, data):
        sensors, y, _ = data
        sensor_coords = list(sensors.keys())
        beacon_coords = list(sensors.values())
        all_objects = set(beacon_coords + sensor_coords)
        ranges = {
            sensor_coord: self.get_manhattan(sensor_coord, beacon_coord)
            for sensor_coord, beacon_coord in sensors.items()
        }

        scanned_ranges = self.scan_row(ranges, y)

        all_range_sum = 0
        for rng in scanned_ranges:
            range_sum = rng[1] - rng[0]
            for position in all_objects:
                if position[1] == y and position[0] >= rng[0] and position[1] <= rng[1]:
                    range_sum -= 1
            all_range_sum += range_sum

        return all_range_sum

    @staticmethod
    def limit_ranges(ranges, m):
        for i in range(len(ranges)):
            f, t = ranges[i]
            f = 0 if f < 0 else f
            t = m if t > m else t
            ranges[i] = (f, t)
        return ranges

    def part_2_logic(self, data):
        sensors, _, m = data
        ranges = {
            sensor_coord: self.get_manhattan(sensor_coord, beacon_coord)
            for sensor_coord, beacon_coord in sensors.items()
        }

        row_objects = {}
        for obj in list(sensors.keys()) + list(sensors.values()):
            if obj[1] not in row_objects:
                row_objects[obj[1]] = []
            row_objects[obj[1]].append(obj[0])

        row_index = 0
        scanned_ranges = []

        for y in range(0, m + 1):
            scanned_ranges = self.scan_row(ranges, y)
            for row_object in row_objects.get(y, []):
                scanned_ranges = self.add_range(
                    scanned_ranges, (row_object, row_object + 1)
                )
            scanned_ranges = self.limit_ranges(scanned_ranges, m)
            if len(scanned_ranges) == 2:
                row_index = y
                break

        for rng in scanned_ranges:
            if rng[0] == 0:
                return (rng[1] * 4000000) + row_index


day = Day()
