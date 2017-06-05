"""
Trying different functions programming tools
"""
import functools
import operator

add_factory = lambda x: functools.partial(operator.add, x)
add5 = add_factory(5)
print(add5(10))