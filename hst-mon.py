#!/usr/bin/python3

import dvb
import sys
import signal
import shutil
import argparse
from subprocess import call
from datetime import datetime, timedelta
from time import sleep


sets = {
        "zuhause": {"Cottaer Straße":3,
        "Hp. Freiberger Straße":10,
        "Tharandter Straße":10}
}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33;1m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


### don't mess up terminal by SIGINT or CTRL^C
def signal_handler(signal,frame):
    call(["tput","cnorm"])
    print("")
    sys.exit(0)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='Fancy DVB Timetable Monitor')
    parser.add_argument('-set',type=str,default="zuhause",help='set of Stations to use')
    parser.add_argument('-help',action="store_true",help="print this help")
    args = parser.parse_args()
    if args.help:
        parser.print_help(sys.stderr)
        exit()
    signal.signal(signal.SIGINT,signal_handler)
    call(["tput","civis"])

    while True:
        lines = shutil.get_terminal_size((85,25)).lines
        if lines%2 == 0:
            lines -= 1
        num = int(lines/len(sets[args.set]))
        sys.stdout.write("\x1B[H\x1B[J")
        sys.stdout.write(bcolors.OKGREEN+"{:<30s}{:<6s}{:<37s}{:>7s}{:>10s}".format("Haltestelle","Linie","Richtung","in","um")+bcolors.ENDC)
        table = []
        for street in sets[args.set]:
            sys.stdout.write("\n")
            monitor = {}
            for elem in dvb.monitor(street,sets[args.set][street],num-1):
                if elem["direction"] not in monitor:
                    monitor[elem["direction"]] = []
                monitor[elem["direction"]].append(elem)
            for direction in monitor:
                now = datetime.now()
                for elem in monitor[direction]:
                    sys.stdout.write("\n{:<30s}".format(street))
                    sys.stdout.write(bcolors.YELLOW+"{:<6s}".format(elem["line"]))
                    sys.stdout.write(bcolors.ENDC+"{:<37s}".format(elem["direction"]))
                    sys.stdout.write("{:>7d} min".format(elem["arrival"]))
                    sys.stdout.write("{:>10s}".format((now+timedelta(minutes=elem["arrival"])).strftime("%H:%M")))
                    sys.stdout.flush()
        sleep(30)
