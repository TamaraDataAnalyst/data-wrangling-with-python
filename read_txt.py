import re
from typing import  List, Iterator
from helpers.map_reduce import map_field
from helpers.take import take_n


######### OPEN AND READ THE DATA FILE ###########
def read_data(filename:str) -> str:
    lines = open(filename)
    for line in lines:
        yield line

LOG_PATTERN = re.compile(r'(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+).*' \
r'(\S+).* (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)'
)

############ DATA TRANSFORMATION #############

def log_file(lines:List[str]) -> Iterator[List[str]]:
    lines = read_data(lines)
    groups = (LOG_PATTERN.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)

    colnames = ('date','time','client_ip','username','server_ip',
    'port','method','stem','query','status','server_bytes',
    'client_bytes','time_taken','user_agent','referrer')

    log = (dict(zip(colnames,t)) for t in tuples)
    log = map_field(log,'server_bytes',int)
    log = map_field(log, 'client_bytes',int)

    return log
    
    ############ DATA QUERYING #############

def print_bytes_transfer(lines):
    log = log_file(lines)
    bytes_over_200000 = (b for b in log
                        if b['client_bytes'] > 200000 and  b['server_bytes'] > 200000)
    for b in bytes_over_200000:
        print('client_ip',b['client_ip'],'client_bytes', b['client_bytes'], 
                'server_bytes',b['server_bytes'])

def total_bytes_sent(lines):
    log = log_file(lines)
    total_bytes = sum(1 for b in log if b['server_bytes'] > 100000)
    print('Total:', total_bytes )


if __name__=='__main__':   
    lines = 'data\log.txt'
    log = print_bytes_transfer(lines)
    print(take_n(log,100))
    
    