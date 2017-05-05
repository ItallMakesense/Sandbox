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

# check = "After this operation, 1,232 kB of additional disk space will be used."
# print(check)
# print(textwrap.fill(check, width=30))
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
#     result = re.findall(r"(\"title\": \".+\")", str(result.read().decode()))
#     print(result)
#     data = lambda : itertools.islice(result, 5)
#     return data

# python = reddit("python")
# golang = reddit("golang")
# for title in python():
#     # print(title)
#     pass
###############################################################################
# def seeker(dictionary, wanted):
#     if isinstance(dictionary, dict):
#         if wanted in dictionary.keys():
#             found = dictionary[wanted]
#         else:
#             for key in dictionary.keys():
#                 found = seeker(dictionary[key], wanted)
#                 if found:
#                     break
#         return found
#     else:
#         return None
def planify(sequence):
    fixed = []
    def repeat(seq):
        if hasattr(seq, '__iter__') and not isinstance(seq, str):
            for item in seq:
                repeat(item)
        else:
            fixed.append(seq)
    repeat(sequence)
    return fixed

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