#!/usr/bin/python3.5

import dvb
import sys
import json
from subprocess import call
from time import sleep

num=4
# Arbeit: streets=["SLUB","TU Dresden","Zellescher Weg"]
streets = ["Cottaer Straße","Rosenstraße","Hp. Freiberger Straße","Tharandter Straße"]
while True:
    #call("clear")
    print("{:<30s}{:<13s}{:<30s}{:>7s}".format("Haltestelle","Linie","Richtung","Ankunft"))
    table=[]
    for street in streets:
        for elem in dvb.monitor(street,0,num,"Dresden"):
            table.append((street,elem["line"],elem["direction"],elem["arrival"]))
    for st, li, di,ar in sorted(table,key=lambda x: x[3]):
        print("{:<30s}{:<13s}{:<30s}{:>7d}".format(st,li,di,ar))
    for i in range(0,num*len(streets)+1):
        sys.stdout.write("\033[F")               
    sleep(2)
