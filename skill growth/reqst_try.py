"""
Loads popular topics from www.reddit.com using closure and generator
"""
import urllib.request as request
import itertools
import re
import pprint

def reddit(search):
    result = request.urlopen("http://www.reddit.com/r/{}.json".format(search))
    result = re.findall(r"\"title\": \"([^\":]+)\"", result.read().decode())
    return lambda: (line for line in result)

python = reddit("python")
golang = reddit("golang")
pprint.pprint(list(itertools.islice(python(), 0, 5)))