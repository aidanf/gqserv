#!/usr/bin/python
#
import socket
import netstring
import sys
import getopt

parms = {'-h': '127.0.0.1', '-p': 8081}
try:
    opts, pargs = getopt.getopt(sys.argv[1:], "h:p:")
except getopt.GetoptError, msg:
    sys.exit(msg)

for o, v in opts:
    print o,v
    parms[o] = v
host = parms['-h']
port = int(parms['-p'])
try:
    file = open(sys.argv[1])
except:
    print "cannot open query file: "
    sys.exit()
    
print "Host:", host, "port:", port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while 1:
    line = file.readline()
    if not line:
        netstring.writens(s, 'BYE')
        break
    if line[-1]=='\n':
        line=line[:-1]
    print "adding query ",line
    
    netstring.writens(s, 'add_query '+line)
    ret = netstring.readns(s)
    print "Server returned: ", ret
s.close()







