"""
Functions for expanding nested sequences.
Second uses the first to return generator.
"""
def planify(sequence):
    shallow_list = []
    def repeat(seq):
        if hasattr(seq, '__iter__') and not isinstance(seq, str):
            for item in seq:
                repeat(item)
        else:
            shallow_list.append(seq)
    repeat(sequence)
    return shallow_list

def planify2(sequence):
    for item in planify(sequence):
        yield item

class MyList(list):
    def __str__(self):
        return "<MyList>"

seq = ('abc', 3, [8, ('x', 'y'), MyList(range(5)), [100, [99, [98, [97]]]]])
print(planify(seq))
gen = planify2(seq)
print(type(gen))
print(list(gen))