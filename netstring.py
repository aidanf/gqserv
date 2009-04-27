#!/usr/bin/python

def readns(sock):
    """read a netstring from a socket."""
    size = ""
    while 1:
        c = sock.recv(1)
        if c == ":":
            break
        elif not c:
            raise IOError, "short netstring read 1"
        size = size + c
    size = sz = int(size)
    s = ""
    while sz:
        ss = sock.recv(sz)
        if not ss:
            raise IOError, "short netstring read 2"
        s += ss
        sz -= len(ss)
    if len(s) != size:
        raise IOError, "short netstring read 3"
    if sock.recv(1) != ",":
        raise IOError, "missing netstring terminator"
    return s

def writens(sock, s):
    """write a netstring to a socket."""
    s = encode(s)
    while len(s):
        l = sock.send(s)
        s = s[l:]

def encode(s):
    return "%d:%s," % (len(s), s)

def decode(s):
    try:
        if s[-1] != ",":
            raise ValueError
        p = s.index(":")
        l = int(s[0:p])
        if len(s) != p + l + 2:
            raise ValueError
        return s[p+1:-1]
    except ValueError:
        raise ValueError, "netstring format error: " + s

def freadns(f):
    """read a netstring from a file."""
    size = ""
    while 1:
        c = f.read(1)
        if c == ":":
            break
        elif not c:
            raise IOError, "short netstring read"
        size = size + c
    size = sz = int(size)
    s = ""
    while sz:
        ss = f.read(sz)
        if not ss:
            raise IOError, "short netstring read"
        s += ss
        sz -= len(ss)
    if len(s) != size:
        raise IOError, "short netstring read"
    if f.read(1) != ",":
        raise IOError, "missing netstring terminator"
    return s

def fwritens(f, s):
    """write a netstring to a file."""
    s = encode(s)
    f.write(s)

