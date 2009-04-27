# Config file for gqserv
# config must be valid python

#start_time and end_time represent the time window during which queries to google
#are allowed. They are represented as a string with format "HHMMSS"
#note the times are localtime
#this start time works
start_time = "014500"
end_time = "101500"

#root_dir is the directory in which gqserv is installed
root_dir = '/nevada/aidan/gqserv'
cache_dir = 'cache'

#log_file is the name of the file to log to.
#an empty string '' results in logging to stdout
log_file = 'log'

#allowed_ip is a list of ip addresses that can send server commands
#e.g. allowed_ip = ['127.0.0.1','127.0.0.2']
#the empty list [] causes the server to accept connections from any ip
allowed_ip = []

#port is the port that the server listens on
port = 8081

#retrieve_delay is the number of seconds to wait between google requests
retrieval_delay = 6
