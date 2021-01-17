for no_processes in 1 3 6 9
do
  for sleep_ms in 1 5 10 15
  do
    echo "processes: $no_processes sleep_ms: $sleep_ms"
    echo "del on_time" | redis-cli
    echo "del delayed" | redis-cli
    date
    for i in $(seq 1 $no_processes)
    do
      screen -S "p1$i" -dm python3 "process_1.py" "$i" "$sleep_ms"
      screen -S "p2$i" -dm python3 "process_2.py" "$i" "$sleep_ms"
      screen -S "p3$i" -dm python3 "process_3.py" "$i" "$sleep_ms"
    done
    date
    sleep 30
    echo "on_time"
    echo "get on_time" | redis-cli
    echo "delayed"
    echo "get delayed" | redis-cli
    pkill screen
  done
done
