"""
Zipper-generator. Missing values are filled-in
with elements of iterable started with beginning.
"""

# from pydoc import locate
def izip_repeat(*iters):
    def extend(seq, max_length):
        end = len(seq)
        for i in range(max_length):
            if i // end:
                i = i % end
            yield seq[i]
    def even_seqs(seq):
        even_seqs = []
        max_length = max((len(sel) for sel in seq))
        for iterable in seq:
            # orig_type = locate(type(iterable).__name__)
            if len(iterable) != max_length:
                even_seqs.append(list(extend(iterable, max_length)))
            else:
                even_seqs.append(iterable)
        return even_seqs
    return (zipped for zipped in zip(*even_seqs(iters)))

g = izip_repeat('abc', [0, 1])
print(type(g), list(g))

print(list(izip_repeat([0, 1, 2], 'mn')))
# [(0, 'm'), (1, 'n'), (2, 'm')]
print(list(izip_repeat('ABCD', 'xy')))
# [('A', 'x'), ('B', 'y'), ('C', 'x'), ('D', 'y')]
print(list(izip_repeat('xy', ['mn', 'op'] , range(5))))
# [('x', 'mn', 0), ('y', 'op', 1), ('x', 'mn', 2), ('y', 'op', 3), ('x', 'mn', 4)]