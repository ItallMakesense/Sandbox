# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup

# driver = webdriver.Chrome()
# driver.get("https://www.lostfilm.tv/")
# assert 'lostfilm' in driver.title.lower()
# elem = driver.find_element_by_name("q")
# elem.send_keys("galactica")
# elem.send_keys(Keys.RETURN)
# soup = BeautifulSoup(driver.page_source)
# print(soup.get_text())
# driver.close()
###############################################################################
# import sqlite3
# import os

# conn = sqlite3.connect(os.getcwd() + '/example.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# conn.commit()
# t = ('RHAT',)
# c.execute('SELECT * FROM stocks WHERE symbol=?', t)
# print(c.fetchone())
# conn.close()
###############################################################################
# import textwrap

# check = "After this operation, 1313 kB of additional disk space will be used."
# print(check)
# print(textwrap.fill(check, width=30))
###############################################################################

###############################################################################
# import functools
# import operator

# add_factory = lambda x: functools.partial(operator.add, x)
# add5 = add_factory(5)
# print(add5(10))
###############################################################################
# import urllib.request as request
# import itertools
# import re

# def reddit(search):
#     result = request.urlopen("http://www.reddit.com/r/{}.json".format(search))
#     result = re.findall(r"(\"title\": \".+\")?", result.read().decode())
#     print(result)
#     data = lambda : itertools.islice(result, 5)
#     return data

# python = reddit("python")
# golang = reddit("golang")
# for title in python():
#     # print(title)
#     pass
###############################################################################
# def planify(sequence):
#     shallow_list = []
#     def repeat(seq):
#         if hasattr(seq, '__iter__') and not isinstance(seq, str):
#             for item in seq:
#                 repeat(item)
#         else:
#             shallow_list.append(seq)
#     repeat(sequence)
#     return shallow_list

# def planify2(sequence):
#     for item in planify(sequence):
#         yield item

# class MyList(list):
#     def __str__(self):
#         return "<MyList>"

# seq = ('abc', 3, [8, ('x', 'y'), MyList(range(5)), [100, [99, [98, [97]]]]])
# print(planify(seq))
# gen = planify2(seq)
# print(type(gen))
# print(list(gen))
###############################################################################
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
###############################################################################

###############################################################################
