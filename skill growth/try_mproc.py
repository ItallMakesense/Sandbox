from collections import Counter
import os
import re


def is_among(name, patterns):
    for pattern in (re.escape(_) for _ in patterns):
        if re.search(pattern.replace('\*', '.*'), name):
            return True
    return False

def match(entry, patterns):
    for p in patterns:
        if p.startswith('*') and entry.endswith(p.lstrip('*')):
            return True
        elif p.endswith('*') and entry.startswith(p.rstrip('*')):
            return True
        elif p == entry:
            return True
    return False

def words_counter(path, glob_patterns, ignored_words, min_word_len):
    files_paths = []
    words = []
    occurs = {}
    with os.scandir(path) as full_dir:
        for entry in full_dir:
            if entry.is_file() and is_among(entry.name, glob_patterns):
                files_paths.append(entry.path)
    print(files_paths)
    for file in files_paths:
        with open(file) as o_file:
            content = (word for word in o_file.read().split()\
                        if not is_among(word, ignored_words) and len(word) >= min_word_len)
    return Counter(content)

words = words_counter(
    path='/var/log',
    glob_patterns=('*log', '*.log'),
    ignored_words=('May', 'ret*'),
    min_word_len=3
    )
print(words)