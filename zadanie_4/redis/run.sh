for i in $(seq 1 10)
do
  screen -S "p1$i" -dm python3 "process_1.py" "$i"
  screen -S "p2$i" -dm python3 "process_2.py" "$i"
  screen -S "p3$i" -dm python3 "process_3.py" "$i"
done
