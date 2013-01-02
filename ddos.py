#!/bin/env python

import subprocess
import re

class NetstatException(Exception):
    pass

def netstat_cmd():
    return [ 'netstat' ]


def netstat_args():
    return [ '-ntu' ]


def netstat_pattern():
    strpat = r'^(tcp|udp)\s*\d+\s*\d+\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    strpat += r':(\d{1,5})\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})\s*'
    strpat += r'([a-zA-Z_]+)\s*$'
    return strpat


def parse_netstat(output):
    lines = output.split("\n")
    pattern = re.compile(netstat_pattern(),re.MULTILINE)
    connList = []
    for line in lines:
        match = pattern.match(line)
        if match != None:
            connList.append( match.groups() )
    return connList


def netstat():
    args = netstat_cmd() + netstat_args()
    proc = subprocess.Popen( args, stdout=subprocess.PIPE )
    output = proc.communicate()[0]  # 0=stdout 1=stderr
    proc.wait()
    if( proc.returncode != 0 ):
        raise NetstatException( 'Netstat didn\'t return 0' )
    return output


def print_connlist(connlist):
    fmtstr = '%5s %15s %15s %15s %15s %15s'
    print fmtstr % ('proto','destip','destport','srcip','srcport','state')
    for conn in connlist:
        print fmtstr % conn


def main():
    print_connlist(parse_netstat(netstat()))
    return 0


if __name__ == "__main__":
    main()


