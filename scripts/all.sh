for entry in ./days/day*.py
do
  echo ""
  echo "----- Running $entry -----"
  python $entry
done
