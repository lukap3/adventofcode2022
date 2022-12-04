days=()
for entry in ./day*.py
do
  echo ""
  echo "----- Running $entry -----"
  python $entry
done
