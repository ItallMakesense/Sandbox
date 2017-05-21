#! /usr/bin/env python
#^

"""
PyNLiS - Python Newbie Linux Search - is a minor analog of Linux grep, that uses
multiprocessing for performing parallel search.
It has a few options implemented:

-R -- recursive search
-n -- print the number of found line
-p -- number of processes (by default number of cores)
Usage example:

$ pynlis.py -R -n 'user' /etc
/etc/pam.d/sshd : 51 : "# to run in the user's context should be run after this."
/etc/pam.d/sudo:3 : "auth       required   pam_env.so readenv=1 user_readenv=0"
"""

from argparse import ArgumentParser
from sys import stderr
import multiprocessing
import os


def pathfinder(path, recursive):
    if recursive:
        handler = lambda e: print("%s - %s" % (e.strerror, e.filename), file=stderr)
        walk_paths = os.walk(path, onerror=handler)
        return (os.path.join(root, file) for (root, dirs, files) in walk_paths\
                for file in files)
    else:
        return (entry.path for entry in os.scandir(path) if entry.is_file())

def searcher(file, word, print_num, line_length, endings="..."):
    with open(file) as o_file:
        for num, line in enumerate(o_file, 1):
            if word in line:
                chunk_length = round((line_length-len(word))/2)
                l_chunk, word, r_chunk = line.strip('\n').partition(word)
                l_chunk = l_chunk[(- chunk_length):]
                r_chunk = r_chunk[:(line_length - len(word) - chunk_length)]
                word = '\033[93m' + word + '\033[0m'
                if print_num:
                    print("%s : %s : {}%s{}".format(endings, endings)\
                            % (file, num, "".join((l_chunk, word, r_chunk))))
                else:
                    print("%s : {}%s{}".format(endings, endings)\
                            % (file, "".join((l_chunk, word, r_chunk))))

def initiate_search(path, word, recursive, print_num, line_len, proc_num):
    pool = multiprocessing.Pool(processes=proc_num)
    for file in pathfinder(path, recursive):
        pool.apply_async(searcher, [file, word, print_num, line_len])


if __name__ == "__main__":
    parser = ArgumentParser(description='pynlis - Python Newbie Linux Search')
    parser.add_argument('-R', dest='rec', action='store_true',\
                        help='recursive search')
    parser.add_argument('-n', dest='num', action='store_true',\
                        help='print the number of found line')
    parser.add_argument('-l', dest='len', default=100, type=int, metavar='length',\
                        help='length of the resulting line (100 chars by default)')
    parser.add_argument('-p', dest='proc', default=multiprocessing.cpu_count(),\
                        type=int, metavar='number',\
                        help='number of processes (number of cores by default)')
    parser.add_argument('word', nargs='?', metavar='Word', help='word to search')
    parser.add_argument('dir', nargs='?', metavar='Directory',\
                        help='directory, where to search')
    args = parser.parse_args()

    initiate_search(path=args.dir, word=args.word, recursive=args.rec,\
                        print_num=args.num, line_len=args.len, proc_num=args.proc)
