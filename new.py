"""
Now it's not so empty ;)
"""
from bs4 import BeautifulSoup
import requests
from pprint import pprint


link = "http://www.petsonic.com/es/perros/snacks-y-huesos-perro"

# Extracting link data, transforming to soup-object
response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')

# Finding "The Button", that shows all products
all_products = soup.find(attrs={'class':'showall pull-left'})
params = {i.get('name') : i.get('value') for i in all_products.find_all('input')}

# Getting data from all-products-link, transforming to soup-object
full_list_link = all_products.get('action')
full_response = requests.get(full_list_link, params=params)
full_soup = BeautifulSoup(full_response.text, 'html.parser')

# Finding products list by given attribute `productlist`
# and writing all references to the separate products into list
prod_links = [line.get('href') for line in full_soup.find_all(attrs={'class':'product-name'}) if line.has_attr('href')]

products = {}

for one_link in prod_links:
    one_response = requests.get(one_link)
    one_soup = BeautifulSoup(one_response.text, 'html.parser')
    one_name = one_soup.find('h1', attrs={'itemprop':'name'})
    name = ''.join(name.strip() for name in one_name.contents if '</a>' not in str(name))
    one_image = one_soup.find('img', id='bigpic').get('src')

    for one in one_soup.find_all(attrs={'class':'attribute_labels_lists'}):
        ending = one.find(attrs={'class':'attribute_name'}).text.strip()
        price = one.find(attrs={'class':'attribute_price'}).text.strip()
        prod_name = "{} - {}".format(name, ending)
        setted = products.setdefault(prod_name, [price, one_image])

pprint(products)
