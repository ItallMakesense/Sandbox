"""
Simple example of a metaclass, which can perform following checks:
- all attributes have snake-case style.
- all user methods do not have empty documentation strings.
- all documentation strings have one space delimiter between words.
"""

import traceback as tb
from re import match as re_match


class Linter(type):

    def __call__(cls, *args, **kwargs):
        namespace = cls.__dict__
        try:
            Linter.case_check(namespace)
            Linter.doc_check(namespace)
            Linter.interval_check(namespace)
        except Exception as e:
            print("Traceback (most recent call last):")
            tb_top = [line for line in tb.format_stack() if '__call__' not in line]
            tb_top.extend(tb.format_tb(e.__traceback__))
            print("".join(tb_top), "LinterError: %s" % e, sep='')
            exit()
        return super().__call__(*args, **kwargs)

    @staticmethod
    def case_check(adict):
        """Checking, if all attributes have snake-case style."""
        for attr in adict:
            if not attr.islower() or not re_match(r"^\w+$", attr):
                raise Exception("Attributes must be snake-cased.")

    @staticmethod
    def doc_check(adict):
        """Checking, if all user methods have
        non-empty documentation strings."""
        for attr in adict:
            if attr not in type.__dict__ and callable(adict[attr]):
                if not hasattr(adict[attr], '__doc__')\
                or not adict[attr].__doc__:
                    raise Exception("\'%s\' has no documentation sting." % attr)

    @staticmethod
    def interval_check(adict):
        """Checking, if all documentation strings have
        one space delimiter between words."""
        for attr in adict:
            if callable(adict[attr])\
            and hasattr(adict[attr], '__doc__'):
                if adict[attr].__doc__\
                and re_match(r"^.*\s{2,}.*$", adict[attr].__doc__.strip()):
                    raise Exception("Documentation strings must have one space interval.")

    # @classmethod
    # def __prepare__(mcs, name, bases, **kwargs):
    #     print('  Linter.__prepare__(mcs=%s, name=%r, bases=%s, kwargs=%s)\n'\
    #             % (mcs, name, bases, kwargs))
    #     return {}

    # def __new__(mcs, name, bases, attrs, **kwargs):
    #     print('  Linter.__new__(mcs=%s, name=%r, bases=%s, attrs=[%s], kwargs=%s)\n'\
    #             % (mcs, name, bases, ', '.join(attrs), kwargs))
    #     return super().__new__(mcs, name, bases, attrs)

    # def __init__(cls, name, bases, attrs, **kwargs):
    #     print('  Linter.__init__(cls=%s, name=%r, bases=%s, attrs=[%s], kwargs=%s)\n'\
    #             % (cls, name, bases, ', '.join(attrs), kwargs))
    #     return super().__init__(name, bases, attrs)


if __name__ == "__main__":

    class Creature(metaclass=Linter):

        def __init__(self, genus):
            self.genus = genus

        def sound(self, msg):
            # """Exception check."""
            print("{0}: {1}".format(self.genus, msg))


    man = Creature("man")
    man.sound("dead")
    print(type(man))
