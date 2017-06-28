from bs4 import BeautifulSoup
import requests


link = "http://www.petsonic.com/es/perros/snacks-y-huesos-perro"

response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')

all_products = soup.find(attrs={'class': 'showall pull-left'})
params = {i.get('name') : i.get('value') for i in all_products.find_all('input')}

full_list_link = all_products.get('action')
full_response = requests.get(full_list_link, params=params)
full_soup = BeautifulSoup(full_response.text, 'html.parser')

prod_list = full_soup.find(attrs={'class': 'productlist'})
prod_links = [line.get('href') for line in prod_list.find_all(attrs={'class': 'product-name'})]

# products = {
#     'Name':,
#     'Price':,
#     'Image'}

one_link = prod_links[0]
one_response = requests.get(one_link)
one_soup = BeautifulSoup(one_response.text, 'html.parser')
one_name = one_soup.find_all(attrs={'class': 'product-name'})
one_image = one_soup.find('img', id='bigpic')
print(one_name, one_image.get('src'))