from advent_day import AdventDay


class Day(AdventDay):
    test_files = {
        "data/day9/example0.txt": [13, 1],
        "data/day9/example1.txt": [88, 36],
    }
    data_file = "data/day9/data.txt"

    directions = {"R": (0, 1), "L": (0, -1), "U": (1, 0), "D": (-1, 0)}

    def follow(self, head_pos, tail_pos):
        hx, hy = head_pos
        tx, ty = tail_pos
        # if head is next to tail do nothing
        if abs(hx - tx) <= 1 and abs(hy - ty) <= 1:
            # do nothing
            return tail_pos
        else:
            ns = [
                # direct neighbours
                [hx + 1, hy],
                [hx, hy + 1],
                [hx - 1, hy],
                [hx, hy - 1],
                # "diagonal" neighbours
                [hx + 1, hy + 1],
                [hx + 1, hy - 1],
                [hx - 1, hy + 1],
                [hx - 1, hy - 1],
            ]
            for n in ns:
                if self.distance(tail_pos, n) <= 1:
                    return n
        raise Exception("unable to follow")

    @staticmethod
    def distance(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return max([abs(x1 - x2), abs(y1 - y2)])

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = data[i].split()
            data[i][1] = int(data[i][1])
        return data

    def part_1_logic(self, moves):
        head_pos = [0, 0]
        tail_pos = [0, 0]
        visited = []

        for move in moves:
            direction, steps = move
            d = self.directions[direction]
            for i in range(steps):
                # move 1 step in direction
                head_pos[0] += d[0]
                head_pos[1] += d[1]

                # move tail towards head
                tail_pos = self.follow(head_pos, tail_pos)
                visited.append(tuple(tail_pos))
        return len(set(visited))

    def part_2_logic(self, moves):
        head_pos = [0, 0]
        tails = []
        visited = []

        for i in range(9):
            tails.append([0, 0])

        for move in moves:
            direction, steps = move
            d = self.directions[direction]
            for i in range(steps):
                # move 1 step in direction
                head_pos[0] += d[0]
                head_pos[1] += d[1]

                # move tail towards head
                tails[0] = self.follow(head_pos, tails[0])
                # move tail toward previous tail
                for j in range(1, len(tails)):
                    tails[j] = self.follow(tails[j - 1], tails[j])
                visited.append(tuple(tails[-1]))

        return len(set(visited))


day = Day()
