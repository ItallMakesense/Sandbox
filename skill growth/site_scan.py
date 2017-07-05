"""

"""
from io import TextIOWrapper
import os
import socket
from tld import get_tld
from urllib.request import urlopen


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

def get_domain_name(url):
    return get_tld(url)

def get_robots_txt(url):
    path = url if url.endswith('/') else url + '/'
    req = urlopen(path + "robots.txt")
    data = TextIOWrapper(req, encoding='utf-8')
    return data.read()

def get_whois(url):
    return str(os.popen("whois %s" % url).read())


if __name__ == "__main__":

    INIT_DIR = "sites"
    create_dir(INIT_DIR)

    def gather_info(name, url):
        sep_dir = "%s/%s" % (INIT_DIR, name)
        create_dir(sep_dir)
        domain_name = get_domain_name(url)
        write_file("%s/%s" % (sep_dir, "url.txt"), url)
        write_file("%s/%s" % (sep_dir, "domain_name.txt"),\
                    domain_name)
        write_file("%s/%s" % (sep_dir, "get_robots.txt"),\
                    get_robots_txt(url))
        write_file("%s/%s" % (sep_dir, "whois.txt"),\
                    get_whois(domain_name))
