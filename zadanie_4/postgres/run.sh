for no_processes in 1 3 6 9
do
  for sleep_ms in 1 5 10 15
  do
    echo "processes: $no_processes sleep_ms: $sleep_ms"
    sleep 3
    psql database < prepare_database.sql
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
    echo "select count(*) as on_time from emissions_on_time" | psql database
    echo "delayed"
    echo "select count(*) as delayed from emissions_delayed" | psql database
    pkill screen
  done
done

