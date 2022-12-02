mkdir data/day$1
touch data/day$1/data.txt
touch data/day$1/example.txt
cp template.py day$1.py
sed -i '' "s/dayX/day$1/" day$1.py
