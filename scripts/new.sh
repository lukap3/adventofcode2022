days=()
for entry in ./day*.py
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
cp template.py day$next.py
sed -i '' "s/dayX/day$next/" day$next.py
