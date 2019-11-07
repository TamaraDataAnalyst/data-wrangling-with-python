from itertools import groupby
from functools import reduce
from typing import List, Any,TypeVar,Iterator

T =TypeVar('T')

def map_field(dictseq:List[T], name:str, func:Any) -> Iterator[List[T]]:
    for d in dictseq:
        d[name] = func(d[name])
        yield d

def _map(func:Any, iterable:List[T]) -> Iterator[List[T]]:
    for i in iterable:
        yield func(i)

def reduceByKey(func:Any, iterable:List[int]) -> List[int]:
    get_key = lambda k: k[0]
    get_value = lambda v: v[1]
    return _map(
        lambda l: (l[0], reduce(func, _map(get_value, l[1]))),
        groupby(sorted(iterable, key=get_key), get_key)
    )

if __name__=='__main__':
    data = [1, 2,3, 4,5, 6]
    expected_result = [(1, 2), (3, 10)]
    my_map= _map(lambda x: x**2, data)
    for m in my_map:
        print(m)
    
        
       


