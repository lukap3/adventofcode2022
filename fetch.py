import os
import sys

import markdownify
import requests
from aocd.models import Puzzle
from bs4 import BeautifulSoup

year = int(sys.argv[1])
day = int(sys.argv[2])

puzzle = Puzzle(year=year, day=day)
data = puzzle.input_data

f = open(f"./data/day{day}/data.txt", "w")
f.write(data + "\n")
f.close()

url = f"https://adventofcode.com/{year}/day/{day}"
cookies = {"session": os.getenv("AOC_SESSION")}
resp = requests.get(url, cookies=cookies)  # type: ignore
soup = BeautifulSoup(resp.content, "html.parser")

instructions = soup.find_all("article", attrs={"class": "day-desc"})
instructions = "\n".join([str(desc) for desc in instructions]) + "\n"

h = markdownify.markdownify(str(instructions), heading_style="ATX")
f = open(f"./data/day{day}/instructions.md", "w")
f.write(h)
f.close()
