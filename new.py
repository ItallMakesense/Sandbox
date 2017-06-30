"""
Now it's not so empty ;)
"""
import csv
import requests
from bs4 import BeautifulSoup


def get_soup(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'html.parser')

def get_all_prods_link(soup):
    all_products = soup.find(attrs={'class':'showall pull-left'})
    params = {i.get('name') : i.get('value') for i in all_products.find_all('input')}
    return all_products.get('action'), params

def get_rich_soup(refined_link):
    link, parameters = refined_link
    response = requests.get(link, params=parameters)
    return BeautifulSoup(response.text, 'html.parser')

prod_links = lambda soup: [
                        line.get('href')\
                        for line in soup.find_all(attrs={'class':'product-name'})\
                        if line.has_attr('href')]

def extract(soup):
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

def write_csv(data):
    global file_name
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == "__main__":

    link = "http://www.petsonic.com/es/perros/snacks-y-huesos-perro"
    file_name = 'petsonic.csv'

    for link in prod_links(get_rich_soup(get_all_prods_link(get_soup(link)))):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        write_csv(extract(soup))
