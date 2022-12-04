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

python day$max.py
