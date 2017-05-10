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
# from flask import Flask, jsonify, request, abort

# app = Flask(__name__)

# students = {"Access time": 1}

# @app.route('/students', methods=['POST'])
# def create_student():
#     new_student = request.args.get('name')
#     if new_student in students:
#         abort(404)
#     students[new_student] = "Created!!!"
#     return jsonify(students)

# @app.route('/students', methods=['GET'])
# def get_all_students():
#     students["Access time"] += 1
#     return jsonify(students)

# @app.route('/students/<id>', methods=['PUT'])
# def update_student_data(id):
#     new_value = request.args.get('value')
#     students[id] = new_value
#     return jsonify({"Result": students})

# @app.route('/students/<id>', methods=['DELETE'])
# def del_student_data(id):
#     del students[id]
#     return jsonify({"Result": students})

# @app.route('/')
# def hello_world():
#     return "A site with students"


# if __name__ == '__main__':
#     app.run()
###############################################################################

###############################################################################
# import functools
# import operator

# add_factory = lambda x: functools.partial(operator.add, x)
# add5 = add_factory(5)
# print(add5(10))
# #############################################################################
# import urllib.request as request
# import itertools
# import re
# import pprint

# def reddit(search):
#     result = request.urlopen("http://www.reddit.com/r/{}.json".format(search))
#     result = re.findall(r"\"title\": \"([^\":]+)\"", result.read().decode())
#     return lambda: (line for line in result)

# python = reddit("python")
# golang = reddit("golang")
# pprint.pprint(list(itertools.islice(python(), 0, 5)))
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
# # from pydoc import locate
# def izip_repeat(*iters):
#     def extend(seq, max_length):
#         end = len(seq)
#         for i in range(max_length):
#             if i // end:
#                 i = i % end
#             yield seq[i]
#     def even_seqs(seq):
#         even_seqs = []
#         max_length = max((len(sel) for sel in seq))
#         for iterable in seq:
#             # orig_type = locate(type(iterable).__name__)
#             if len(iterable) != max_length:
#                 even_seqs.append(list(extend(iterable, max_length)))
#             else:
#                 even_seqs.append(iterable)
#         return even_seqs
#     return (zipped for zipped in zip(*even_seqs(iters)))

# g = izip_repeat('abc', [0, 1])
# print(type(g), list(g))

# print(list(izip_repeat([0, 1, 2], 'mn')))
# # [(0, 'm'), (1, 'n'), (2, 'm')]
# print(list(izip_repeat('ABCD', 'xy')))
# # [('A', 'x'), ('B', 'y'), ('C', 'x'), ('D', 'y')]
# print(list(izip_repeat('xy', ['mn', 'op'] , range(5))))
# # [('x', 'mn', 0), ('y', 'op', 1), ('x', 'mn', 2), ('y', 'op', 3), ('x', 'mn', 4)]
###############################################################################

###############################################################################
# import sys,os
# import curses

# def draw_menu(stdscr):
#     k = 0
#     cursor_x = 0
#     cursor_y = 0

#     # Clear and refresh the screen for a blank canvas
#     stdscr.clear()
#     stdscr.refresh()

#     # Start colors in curses
#     curses.start_color()
#     curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
#     curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
#     curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

#     # Loop where k is the last character pressed
#     while k != ord('q'):

#         # Initialization
#         stdscr.clear()
#         height, width = stdscr.getmaxyx()

#         if k == curses.KEY_DOWN:
#             cursor_y = cursor_y + 1
#         elif k == curses.KEY_UP:
#             cursor_y = cursor_y - 1
#         elif k == curses.KEY_RIGHT:
#             cursor_x = cursor_x + 1
#         elif k == curses.KEY_LEFT:
#             cursor_x = cursor_x - 1

#         cursor_x = max(0, cursor_x)
#         cursor_x = min(width-1, cursor_x)

#         cursor_y = max(0, cursor_y)
#         cursor_y = min(height-1, cursor_y)

#         # Declaration of strings
#         title = "Curses example"[:width-1]
#         subtitle = "Written by Clay McLeod"[:width-1]
#         keystr = "Last key pressed: {}".format(k)[:width-1]
#         statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
#         if k == 0:
#             keystr = "No key press detected..."[:width-1]

#         # Centering calculations
#         start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
#         start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
#         start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
#         start_y = int((height // 2) - 2)

#         # Rendering some text
#         whstr = "Width: {}, Height: {}".format(width, height)
#         stdscr.addstr(0, 0, whstr, curses.color_pair(1))

#         # Render status bar
#         stdscr.attron(curses.color_pair(3))
#         stdscr.addstr(height-1, 0, statusbarstr)
#         stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
#         stdscr.attroff(curses.color_pair(3))

#         # Turning on attributes for title
#         stdscr.attron(curses.color_pair(2))
#         stdscr.attron(curses.A_BOLD)

#         # Rendering title
#         stdscr.addstr(start_y, start_x_title, title)

#         # Turning off attributes for title
#         stdscr.attroff(curses.color_pair(2))
#         stdscr.attroff(curses.A_BOLD)

#         # Print rest of text
#         stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
#         stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
#         stdscr.addstr(start_y + 5, start_x_keystr, keystr)
#         stdscr.move(cursor_y, cursor_x)

#         # Refresh the screen
#         stdscr.refresh()

#         # Wait for next input
#         k = stdscr.getch()

# def main():
#     curses.wrapper(draw_menu)

# if __name__ == "__main__":
#     main()
###############################################################################
from flask import Flask, jsonify, request, abort
import datetime

app = Flask(__name__)

list_of = {"jobs": [], "statuses": [], "results": []}
# job_id = 0
# def get_id():
#     global job_id
#     job_id += 1
#     return job_id

@app.route('/api/jobs', methods=['GET'])
def get_jobs_list():
    return jsonify(list_of["jobs"])

@app.route('/api/jobs', methods=['POST'])
def create_job():
    job_id = len(list_of["jobs"]) + 1
    list_of["jobs"].append({
        "job_id": job_id,
        "command": request.json.get("command"),
        "created": str(datetime.datetime.now()).\
                   replace(" ", datetime.date.today().strftime("%A")[0])
    })
    list_of["statuses"].append({
        "status_id": job_id,
        "done": False
    })
    return "{} {}\n{}".format(request.environ.get('SERVER_PROTOCOL'),\
           "202 Accepted", job_status_url(job_id))

@app.route('/api/jobs/<job_id>', methods=['GET'])
def job_status_url(job_id):
    if job_id <= len(list_of["statuses"]) and job_id > 0:
        return "Location: /api/statuses/{}\n".format(job_id)
    else:
        return "No location for that job"

@app.route('/api/jobs/<job_id>', methods=['DELETE'])
def remove_job():
    pass

@app.route('/api/statuses', methods=['GET'])
def all_jobs_statuses():
    return jsonify(list_of["statuses"])

@app.route('/api/statuses/<job_id>', methods=['GET'])
def job_status(job_id):
    if job_id <= len(list_of["statuses"]) and job_id > 0:
        if list_of["statuses"][job_id]["done"]:
            return "{} {}\nLocation: {}\n".format(request.environ.get('SERVER_PROTOCOL'),\
                   "303 See Other", "/api/results/{}".format(job_id))
        else:
            return "{} {}".format(request.environ.get('SERVER_PROTOCOL'), "200 Ok")
    else:
        return "{} {}\nWrong address".format(request.environ.get('SERVER_PROTOCOL'),\
               "404 Not found")

@app.route('/api/results', methods=['GET'])
def all_jobs_results():
    return jsonify(list_of["results"])

@app.route('/api/results/<job_id>', methods=['GET'])
def job_result(job_id):
    result_id = len(list_of["results"]) + 1
    if job_id <= len(list_of["statuses"]) and job_id > 0:
        pass


@app.route('/api/results/<job_id>', methods=['DELETE'])
def remove_job_result(job_id):
    pass

# @app.route('/students', methods=['GET'])
# def get_all_students():
#     students["Access time"] += 1
#     return jsonify(students)

# @app.route('/students/<id>', methods=['PUT'])
# def update_student_data(id):
#     new_value = request.args.get('value')
#     students[id] = new_value
#     return jsonify({"Result": students})

# @app.route('/students/<id>', methods=['DELETE'])
# def del_student_data(id):
#     del students[id]
#     return jsonify({"Result": students})

# @app.route('/')
# def hello_world():
#     return "A site with students"


if __name__ == '__main__':
    app.run()