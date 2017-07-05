"""
Simple script, allowing to see the scrap order of some element
of the site.
By default it's given that address:
 - http://www.petsonic.com/es/perros/snacks-y-huesos-perro -
so afterwords the script seeks each product on this page,
extracts it's name (different names for different products scales on the same page),
it's price and images - and writes all this info into CSV file with this name:
 - petsonic.csv
"""
import csv
import requests
import argparse
from bs4 import BeautifulSoup
import concurrent.futures as conf
from itertools import repeat


def get_soup(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'html.parser')

def get_link_to_all(soup):
    all_products = soup.find(attrs={'class':'showall pull-left'})
    params = {i.get('name') : i.get('value') for i in all_products.find_all('input')}
    return all_products.get('action'), params

def get_rich_soup(refined_link):
    link, parameters = refined_link
    response = requests.get(link, params=parameters)
    return BeautifulSoup(response.text, 'html.parser')

def get_all_links(soup):
    return [line.get('href') for line in\
            soup.find_all(attrs={'class':'product-name'})\
            if line.has_attr('href')]

def extract_data(soup):
    for name in soup.find('h1', attrs={'itemprop':'name'}).contents:
        if '</a>' not in str(name):
            prod_name = name.strip()
    image = soup.find('img', id='bigpic').get('src')
    result = []
    for i in soup.find_all(attrs={'class':'attribute_labels_lists'}):
        ending = i.find(attrs={'class':'attribute_name'}).text.strip()
        price = i.find(attrs={'class':'attribute_price'}).text.strip()
        name = "{} - {}".format(prod_name, ending)
        result.append((name, price, image))
    return result

def write_csv(data, file_name):
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def single_product_write(link_and_file):
    link, file = link_and_file
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    write_csv(extract_data(soup), file)


if __name__ == "__main__":

    _link = "http://www.petsonic.com/es/perros/snacks-y-huesos-perro"
    _file_name = 'petsonic.csv'

    parser = argparse.ArgumentParser(description="Site product scrapper")
    parser.add_argument('link', default=_link, nargs='?',\
                        help="URL of target site (default isjust example: %s)"\
                        % _link)
    parser.add_argument('file', default=_file_name, nargs='?',\
                        help="Path to .csv output file (default is just example: %s)"\
                        % _file_name)
    args = parser.parse_args()

    links = get_all_links(get_rich_soup(get_link_to_all(get_soup(args.link))))
    
    executor = conf.ProcessPoolExecutor()
    executor.map(single_product_write, zip(links, repeat(args.file, len(links))))
