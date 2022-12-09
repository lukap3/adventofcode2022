days=()
for entry in days/day*.py
do
  dayNum="${entry//[^0-9]/}"
  days+=("$dayNum")
done

max=${days[0]}
for n in "${days[@]}" ; do
    ((n > max)) && max=$n
done
next=$((max+1))

echo "Generating day $next"

mkdir data/day$next
touch data/day$next/data.txt
touch data/day$next/example.txt
cp template days/day$next.py
sed -i '' "s/dayX/day$next/" days/day$next.py

python fetch.py ${YEAR} $next
