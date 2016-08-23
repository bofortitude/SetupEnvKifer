#!/usr/bin/python

import sys

from AdcCommandLine import TelnetCommandLine



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:'
        print ''
        print './AdcCmd.py <ADC_IP> <CMD_File>'
        print ''
        exit()

    my_cmd = TelnetCommandLine(sys.argv[1])
    my_cmd.run_cmd_file(sys.argv[2])
