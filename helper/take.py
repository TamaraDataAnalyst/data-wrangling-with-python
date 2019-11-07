from itertools import islice

def take_n(iterable, nlines):
    for i in islice(iterable,nlines):
        yield i
           
        
    