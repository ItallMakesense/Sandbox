from collections import Counter
import multiprocessing
import os


occurs = Counter()

def among(name, patterns):
    """ Makes sense of constructions like *his or thi*.
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
    return match

def multi_counter(file, ignored, min_len):
    with open(file, encoding="utf8") as o_file:
        try:
            content = (word for word in o_file.read().split()\
                        if not among(word, ignored)\
                        and len(word) >= min_len)
            occurs.update(Counter(content))
        except UnicodeError as error:
            print("{} - Unsupported text file. Error message:\n{}".format(\
                    file, error))

def words_counter(path, glob_patterns, ignored_words, min_word_len):
    files_paths = []
    for entry in os.scandir(path):
        if entry.is_file() and among(entry.name, glob_patterns):
            files_paths.append(entry.path)
    print(files_paths)
    for file in files_paths:
        # mproc = multiprocessing.Process(target=multi_counter,\
        #         args=(file, ignored_words, min_word_len))
        # mproc.start()
        multi_counter(file, ignored_words, min_word_len)
    return dict(occurs)

words = words_counter(
    path='D:/ProcessExplorer',
    # path='/usr/bin',
    glob_patterns=('py*', '*.txt'),
    ignored_words=('import', 'from', 'def*', 'con*', '*if'),
    min_word_len=3
    )
for n, k in enumerate(sorted(words)):
    try:
        print(k)
        print(n)
    except:
        print("__________________________________________")
        print(n)
        continue