#!/bin/env python

import subprocess

class NetstatException(Exception):
    pass

def netstat_cmd():
    return [ 'netstat' ]


def netstat_args():
    return [ '-ntu' ]


def netstat():
    args = netstat_cmd() + netstat_args()
    proc = subprocess.Popen( args, stdout=subprocess.PIPE )
    output = proc.communicate()[0]  # 0=stdout 1=stderr
    proc.wait()
    if( proc.returncode != 0 ):
        raise NetstatException( 'Netstat didn\'t return 0' )
    return output


def main():
    print netstat()
    return 0


if __name__ == "__main__":
    main()


