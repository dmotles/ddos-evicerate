#!/bin/env python

import subprocess
import re

"""*nix netstat scraper implementation(s)"""

class NetstatException(Exception):
    """
    Thrown whenever there's a netstat issue.
    """
    pass


class Netstat:
    """
    An abstract class that will define netstat scraper implementation.

    Extend this class to provide netstat scraper support on a per-OS basis.
    """

    def get_output(self):
        """Returns a string of output from netstat command (or equivelant)."""
        raise NotImplementedError("netstat should be implemented!")


    def parse(self,ouput):
        """
        Returns a list of tuples that contain current active connections.

        Tuple format should be (proto,destip,destport,srcip,srcport,state).
        """
        raise NotImplementedError("parse_netstat should be implemented!")


class RhelNetstat(Netstat):
    """
    An implementation of the netstat scraper for CentOS/RHEL.

    This is the default class.
    """

    def cmd(self):
        return [ 'netstat' ]


    def args(self):
        return [ '-ntu' ]


    def pattern(self):
        strpat = r'^(tcp|udp)\s*\d+\s*\d+\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        strpat += r':(\d{1,5})\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})'
        strpat += r'\s*([a-zA-Z_]+)\s*$'
        return strpat


    def parse(self,output):
        lines = output.split("\n")
        pattern = re.compile(self.pattern(),re.MULTILINE)
        connList = []
        for line in lines:
            match = pattern.match(line)
            if match != None:
                connList.append( match.groups() )
        return connList


    def get_output(self):
        args = self.cmd() + self.args()
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
    netstat = RhelNetstat()
    output = netstat.get_output()
    connlist = netstat.parse(output)
    print_connlist(connlist)
    return 0


if __name__ == "__main__":
    main()


