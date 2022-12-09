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
resp = requests.get(url)

soup = BeautifulSoup(resp.content, "html.parser")
desc = soup.find("article", attrs={"class": "day-desc"})

h = markdownify.markdownify(str(desc), heading_style="ATX")
f = open(f"./data/day{day}/instructions.md", "w")
f.write(h)
f.close()
