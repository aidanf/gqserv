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

print "Host:", host, "port:", port
print "Type help for help"
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
except:
    print "cant connect to host ",host," on port ",port
    sys.exit()
while 1:
    try:
        arg = raw_input("Send: ")
    except KeyboardInterrupt:
        netstring.writens(s, 'BYE')
        break
    if not arg:
        continue
    netstring.writens(s, arg)
    ret = netstring.readns(s)
    print "Returned:", ret
s.close()

