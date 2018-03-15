#!/usr/bin/python3.5

import dvb
import sys
import signal
import shutil
import os
import argparse
import json
from subprocess import call
from time import sleep


station=None
stations={
"arbeit":  ["SLUB","TU Dresden","Zellescher Weg"],
"zuhause": ["Cottaer Straße","Rosenstraße","Hp. Freiberger Straße","Tharandter Straße"],
"hbf":     ["Hauptbahnhof","Hauptbahnhof Nord"]
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
    lines=shutil.get_terminal_size((85,25)).lines
    num=int(shutil.get_terminal_size((80,25)).lines/len(stations[station]))
    for i in range(0,num*len(stations[station])):
        print("")
    sys.exit(0)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='Fancy DVB Timetable Monitor')
    parser.add_argument('-set',type=str,default="zuhause",help='set of Stations to use')
    parser.add_argument('-help',action="store_true",help="print this help")
    args=parser.parse_args()
    if args.set:
        station=args.set
    args=parser.parse_args()
    if args.help:
        parser.print_help(sys.stderr)
        exit()
    signal.signal(signal.SIGINT,signal_handler)
    while True:
        lines=shutil.get_terminal_size((85,25)).lines
        if lines%2==0:
            lines-=1
        rows=shutil.get_terminal_size((85,25)).columns
        num=int(lines/len(stations[station]))
        #if num==shutil.get_terminal_size((80,25)).lines/len(stations[station]):
            #num-=2
        #else:
            #num-=1
        #call("clear")
        sys.stdout.write("\x1B[H\x1B[J")
        sys.stdout.write(bcolors.OKGREEN+"{:<30s}{:<13s}{:<30s}{:>7s}".format("Haltestelle","Linie","Richtung","Ankunft")+bcolors.ENDC)
        table=[]
        for street in stations[station]:
            sys.stdout.write("\n")
            for elem in dvb.monitor(street,1,num-1,"Dresden"):
                sys.stdout.write("\n{:<30s}".format(street)+bcolors.YELLOW+"{:<13s}".format(elem["line"])+bcolors.ENDC+"{:<30s}".format(elem["direction"])+"{:>7d}".format(elem["arrival"]))
        sleep(10)
        #table.append((street,elem["line"],elem["direction"],elem["arrival"]))
            
#        for st, li, di,ar in sorted(table,key=lambda x: x[3]):
        #for st, li, di,ar in table:
        #    sys.stdout.write("\n{:<30s}".format(st)+bcolors.YELLOW+"{:<13s}".format(li)+bcolors.ENDC+"{:<30s}".format(di)+"{:>7d}".format(ar))
        
