#!/usr/bin/python
#
# Written by Aidan Finn April 2002
# version 0.1
#
# TODO: README, client that reads a list of queries from a file
# TODO: help command, add_query_force

import SocketServer
import netstring
import sys, os
import string
import time
import threading
import urllib
from config import *

def now():
    return time.ctime(time.time())

def now_str():
    return time.strftime("%H%M%S",time.localtime(time.time()))

class googleDaemon(threading.Thread):
    def __init__(self,start,end,daemon_del=120,retrieve_del=10):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self.ok_start_time = time.strptime(start,"%H%M%S")
        self.ok_end_time = time.strptime(end,"%H%M%S")
        self.daemon_delay = daemon_del
        self.retrieve_delay = retrieve_del
        
    def ok_to_run(self):
        #assume start and finish on same day
        t = time.localtime(time.time())

        t_s = int(t[3])*3600.0 + (t[4])*60.0 + (t[5])
        start_s = int(self.ok_start_time[3])*3600.0 + (self.ok_start_time[4])*60.0 + (self.ok_start_time[5])
        end_s = int(self.ok_end_time[3])*3600.0 + (self.ok_end_time[4])*60.0 + (self.ok_end_time[5])
        
        if t_s > start_s and t_s < end_s and MyRequestHandler.queue:
            return 1
        else:
            return 0
    
    def run(self):
        while 1:
            if self.ok_to_run():
                while 1:
                    if not self.ok_to_run():
                        break
                    if not MyRequestHandler.queue:
                        break
                    query, MyRequestHandler.queue = MyRequestHandler.queue[0], MyRequestHandler.queue[1:]
                    try:
                        q = string.strip(string.replace(query,'_',' '))
                        params = string.split(q,'param:')[1:]
                        q = string.strip(string.split(q,'param:')[0])
                        q = 'http://www.google.com/search?output=xml&client=research_projects&q='+urllib.quote(q)
                        for p in params:
                            q = q + '&' + string.strip(p)
                        print now()," Retrieving query ",q
                        res = urllib.urlopen(q).read()
                        f = open(os.path.join(root_dir,cache_dir,query),'w')
                        f.write(res)
                        f.close
                        time.sleep(self.retrieve_delay)
                    except:
                        print now()," Failed retrieving query: ",query
                time.sleep(self.retrieve_delay)
            else:
                t = time.localtime(time.time())
                t_s = int(t[3])*3600.0 + (t[4])*60.0 + (t[5])
                start_s = int(self.ok_start_time[3])*3600.0 + (self.ok_start_time[4])*60.0 + (self.ok_start_time[5])

                if start_s > t_s:
                    sleep_len = start_s - t_s
                elif start_s < t_s:
                    sleep_len = 86400.0 - t_s -start_s
                else:
                    sleep_len=0
                sleep_len = max(sleep_len,self.daemon_delay)
                
                time.sleep(sleep_len) # could calculate the length of the delay
                
class MyRequestHandler(SocketServer.BaseRequestHandler):
    queue = []
        
    def handle(self):
        print now()," Connected:", self.client_address
        if allowed_ip and self.client_address[0] not in allowed_ip:
            print "client address not allowed: ",self.client_address
            netstring.writens(self.request, '0 UNAUTHORISED IP:'+self.client_address[0])
            return
        while 1:            
            rq = netstring.readns(self.request)
            print now(), ' ',self.client_address, ' ',rq
            sys.stdout.flush()
            if rq == "BYE":
                break
            command = string.split(rq)[0]
            if command == 'add_query':
                self.add_query(rq[len(command)+1:])
            elif command == 'add_query_force':
                self.add_query_force(rq[len(command)+1:])                
            elif command == 'retrieve_query':
                self.retrieve_query(rq[len(command)+1:])
            elif command == 'queue_stat':
                self.queue_stat()
            elif command == 'queue_contents':
                self.queue_contents()
            elif command == 'cache_contents':
                self.cache_contents()
            elif command == 'help':
                self.print_help()
            else:
                netstring.writens(self.request, '0 UNKNOWN COMMAND:'+command)

    def add_query(self,query):
        q = self.encode_query(query)
        if os.path.exists(os.path.join(root_dir,cache_dir,q)):
            netstring.writens(self.request, 'O ALREADY IN CACHE: '+q)
        elif not q in MyRequestHandler.queue:
            MyRequestHandler.queue.append(q)
            netstring.writens(self.request, '1 ADDED: '+q)
        else:
            netstring.writens(self.request, 'O ALREADY IN QUEUE: '+q)
            
    def add_query_force(self,query):
        q = self.encode_query(query)
        if not q in MyRequestHandler.queue:
            MyRequestHandler.queue.append(q)
            netstring.writens(self.request, '1 ADDED: '+q)
        else:
            netstring.writens(self.request, 'O ALREADY IN QUEUE: '+q)
            
    def retrieve_query(self,query):
        q = self.encode_query(query)
        try:
            res = open(os.path.join(root_dir,cache_dir,q),'r').read()
        except IOError:
            res = '0 QUERY NOT IN CACHE '+q
        netstring.writens(self.request, res)
        
    def queue_stat(self):
        ret = str(len(MyRequestHandler.queue)) + ' items in queue'
        netstring.writens(self.request, ret)

    def queue_contents(self):
        netstring.writens(self.request, str(MyRequestHandler.queue))

    def cache_contents(self):
        netstring.writens(self.request, str(os.listdir(os.path.join(root_dir,cache_dir))))

    def encode_query(self,query):
        eq = ''
        terms = string.split(query)
        for x in terms:
            eq = eq + string.strip(string.lower(x)) + '_'
        return eq
    
    def print_help(self):
        help_str = """
        Detailed instructions are in the file /nevada/aidan/gqserv/README.ps
        Available commands:
          add_query [keyword1 keyword2 ...] [param: parameter1 param: parameter2 ...]
          add_query_force [keyword1 keyword2 ...] [param: parameter1 param: parameter2 ...]
          retrieve_query [keyword1 keyword2 ...] [param: parameter1 param: parameter2 ...]
          queue_stat
          queue_contents
          cache_contents
          help
        """
        netstring.writens(self.request, help_str)

print now()," Starting query server"
myServer = SocketServer.ThreadingTCPServer(('', port),MyRequestHandler)
print "listening on port ",port
print "retrieval between ",start_time," and",end_time," localtime"
print "delay between retrieval requests: ",retrieval_delay
if allowed_ip:
    print "allowing connections from ",allowed_ip
g = googleDaemon(start_time,end_time,retrieve_del=retrieval_delay)
print "Starting retrieval thread"
g.start()
if log_file:
    print "logging to ",os.path.join(root_dir,log_file)
    sys.stdout = open(os.path.join(root_dir,log_file),'a')

while 1:
    try:
        myServer.handle_request()
    except KeyboardInterrupt:
        sys.exit()



















