#!/usr/bin/python

import sys
import ConfigParser
import re
import ClearServerNetConfig
import SshRemote


def setupEnv(topologyFile):
    conf = ConfigParser.ConfigParser()
    conf.read(topologyFile)

    sectionList = conf.sections()
    for i in sectionList:
        if not conf.has_option(i, 'ip'):
            print 'Node '+i+' has no "ip" option, skip the operation of this node!'
            continue
        serverIp = conf.get(i, 'ip')
        if not conf.has_option(i, 'port'):
            serverPort = 22
        else:
            serverPort = int(conf.get(i, 'port'))
        if not conf.has_option(i, 'username'):
            username = 'root'
        else:
            username = conf.get(i, 'username')
        if not conf.has_option(i, 'password'):
            password = 'fortinet'
        else:
            password = conf.get(i, 'password')

        cmdSequenceListRaw = []
        optionList = conf.options(i)
        cmdPattern = re.compile(r'^cmd[0-9]+$')
        for j in optionList:
            if cmdPattern.match(j):
                cmdSequenceListRaw.append(int(j.replace('cmd', '')))

        cmdSequenceList = sorted(cmdSequenceListRaw)

        print 'Starting to configure the server "'+serverIp+'" ...'
        ClearServerNetConfig.clearNetworkConfig(serverIp, username=username, passwd=password, serverPort=serverPort)
        ClearServerNetConfig.initNetworkConfig(serverIp, username=username, passwd=password, serverPort=serverPort)
        mySshAgent = SshRemote.SshAgent(serverIp, username, password, remotePort=serverPort)
        mySshAgent.connectRemote()
        for j in cmdSequenceList:
            mySshAgent.execCommand(conf.get(i, 'cmd'+str(j)))
        mySshAgent.closeSsh()
        print 'Configuring server "'+serverIp+'" over.'



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ''
        print 'Usage:'
        print './SetupEnv.py <Topology File>'
        print '''
Topology File example:

[Client1]
ip = 10.0.12.11
cmd1 = ls
cmd2 = ip add add 10.76.1.11/16 dev eth1.1001

[Server1]
ip = 10.0.12.21
port = 22
username = root
password = fortinet
cmd1 = ip route add 200.1.1.0/24 via 10.78.1.1
        '''
        print ''
        exit()

    setupEnv(sys.argv[1])






