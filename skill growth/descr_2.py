"""
Example for DocAPI usage.
"""

from doclib import DocAPI


class Foo(object):

    __doc__ = DocAPI()

    def __init__(self, x):
        self.x = x

    def meth(self, y):
        """Multiplies two values self.x and y."""
        return self.x * y


if __name__ == "__main__":

    print(Foo.__doc__)
# meth : Multiplies two values self.x and y.
    foo = Foo(10)
    print(foo.__doc__)
# meth : Multiplies two values self.x and y.
# x : 10
