import sys
import csv
import datetime
import time
import argparse
from subprocess import Popen, PIPE


class Watcher:
    def __init__(self, cmd, time_interval, filename):
        self.cmd = cmd
        self.time_interval = time_interval
        self.filename = filename
        self.outputfile = open(filename, 'w')
        self.writer = csv.writer(self.outputfile)
        self.meminfo_keys = list(self.parse_meminfo().keys())
        self.writer.writerow(['timestamp'] + self.meminfo_keys)

    @staticmethod
    def parse_meminfo():
        with open('/proc/meminfo') as meminfo:
            lines = meminfo.readlines()
        result = {}
        for line in lines:
            name, value = line.split(':')
            value = value.strip()
            if value.endswith('kB'):
                value = int(value[:-2])*1000
            else:
                value = int(value)
            result[name] = value
        return result

    def add_measure(self):
        meminfo = self.parse_meminfo()
        timestamp = str(datetime.datetime.now())
        self.writer.writerow([timestamp] + [meminfo[k] for k in self.meminfo_keys])

    def run_and_watch(self):
        self.add_measure()
        proc = Popen(self.cmd, stdout=PIPE, stderr=PIPE)
        while proc.poll() is None:
            time.sleep(self.time_interval)
            self.add_measure()
        stdout, stderr = proc.communicate()
        sys.stdout.write(stdout.decode())
        sys.stderr.write(stderr.decode())
        self.outputfile.flush()
        sys.exit(proc.returncode)


def main(args):
    parser = argparse.ArgumentParser(description='Monitoring of a command memory consumption')
    parser.add_argument('--time_interval', '-t', type=int, default=1,
                        help='Period of the measures, in seconds')
    parser.add_argument('--output', '-o', type=str, default='/tmp/memwatch.csv',
                        help='Output file for the measures')
    parser.add_argument('command', type=str,
                        help='Command line to execute')
    args = parser.parse_args(args)
    watcher = Watcher(cmd=args.command.split(), time_interval=args.time_interval, filename=args.output)
    watcher.run_and_watch()


if __name__ == '__main__':
    main(sys.argv[1:])
