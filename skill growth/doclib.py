import inspect


class DocAPI(object):

    def __init__(self):
        self.docstring = ""

    def api(self, obj):
        attrs = list(filter(lambda a: not a.startswith('_'), dir(obj)))
        print("In API:", attrs)
        for attr in attrs:
            if inspect.ismethod(getattr(obj, attr)):
                print("%s : %s\n" % (attr, eval('obj.{}.__doc__'.format(attr))))
                self.docstring += "%s : %s\n" % (attr, eval('obj.{}.__doc__'.format(attr)))
            else:
                print("%s : %s\n" % (attr, eval('obj.{}'.format(attr))))
                self.docstring += "%s : %s\n" % (attr, eval('obj.{}'.format(attr)))
        # return dict(zip(attrs, (eval('obj.%s' % attr) for attr in attrs)))
        # return {"meth" : eval('obj.meth')}
        # p = eval('obj.%s' % list(attrs)[0])
        # return p

    def __get__(self, obj, obj_type):
        print("In GET:", obj, obj_type)
        if not obj:
            self.api(obj_type)
            # return obj_type.meth.__doc__
            return self.docstring
        else:
            self.api(obj)
            # return self.api(obj)
            return self.docstring
