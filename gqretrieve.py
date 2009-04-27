#!/usr/bin/python
#
import socket
import netstring
import sys
import getopt
import string

def encode_query(query):
    eq = ''
    terms = string.split(query)
    for x in terms:
        eq = eq + string.strip(string.lower(x)) + '_'
    return eq


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
    print "Cannot open query file: "
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
    print "retrieving query ",line
    
    netstring.writens(s, 'retrieve_query '+line)
    ret = netstring.readns(s)
    if ret[0] == '0':
        print ret
    else:
        f = open(encode_query(line),'w')
        f.write(ret)
s.close()
