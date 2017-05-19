"""
This script counts occurrence of words in text files in specified path,
using multiprocessing module.
"""
from collections import Counter
import multiprocessing
import os
import time


def among(name, patterns):
    """
    Filter constructions like *his or thi*.
    """
    match = False
    for pattern in patterns:
        if pattern == '*':
            match = name == pattern
        elif pattern.startswith('*'):
            match = name.endswith(pattern[1:])
        elif pattern.endswith('*'):
            match = name.startswith(pattern[:-1])
        elif name == pattern:
            match = True
        if match:
            return match

def multi_counter(ns, file, ignored, min_len):
    """
    Opens file and counts an amount of each word occuring
    in it. In the end updates common counter for all of parallel
    processes. Raises an error, if file includes undecodable symbols.
    """
    counter = ns.occurs
    with open(file) as o_file:
        try:
            content = (word for word in o_file.read().split()\
                        if not among(word, ignored)\
                        and len(word) >= min_len)
            counter.update(Counter(content))
            ns.occurs = counter
        except UnicodeError as error:
            print("{} - Unsupported text file. Error message:\n{}".format(\
                    file, error))

def words_counter(path, glob_patterns, ignored_words, min_word_len):
    """
    Main function for counting word occurances.
    Creates generator list of needed files files_paths
    and using multiprocessing for count words in each file
    in a separate process. Waits for one process' end to start another.
    Returns Counter() object.
    """
    manager = multiprocessing.Manager()
    namespace = manager.Namespace()
    namespace.occurs = Counter()
    files_paths = (entry.path for entry in os.scandir(path)\
                    if entry.is_file() and among(entry.name, glob_patterns))
    for file in files_paths:
        mproc = multiprocessing.Process(target=multi_counter,\
                args=(namespace, file, ignored_words, min_word_len))
        mproc.start()
        mproc.join()
    return namespace.occurs


if __name__ == "__main__":
    words = words_counter(
        path='/usr/bin',
        glob_patterns=('py*', '*.txt'),
        ignored_words=('import', 'from', 'def*', 'con*', '*if'),
        min_word_len=3
        )
    for word, count in words.most_common(50):
        print("{} - {}".format(word, count))
