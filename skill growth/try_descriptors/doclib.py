"""
Non-data descriptor, which can provide class-level and
instance-level documentation about user methods and attributes.

See module usage in descr_2.py
"""

class DocAPI(object):

    def __get__(self, obj, obj_type):
        filter_func = lambda attr: not attr.startswith('__')
        out_line = {}
        if obj:
            ns = set(filter(filter_func, dir(obj_type) + dir(obj)))
        else:
            ns = filter(filter_func, obj_type.__dict__)
            obj = obj_type
        for attr in ns:
            value = getattr(obj, attr)
            if callable(value):
                value = value.__doc__
            out_line.update({attr : str(value)})
        listed_line = (" : ".join(items) for items in out_line.items())
        return "\n".join(listed_line)
