Run a command line while monitoring the memory consumption (using the file `/proc/meminfo`).

For example, this will run the command `sleep 5` while measuring the memory consumption every 2 seconds and storing the
result in file `/tmp/memdata.csv` :
```shell
python memwatch.py -t 2 -o /tmp/memdata.csv "sleep 5"
```

Note that this is the *total* memory consumption of the system, it will also be affected by other processes.
