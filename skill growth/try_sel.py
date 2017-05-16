"""
Using Selemium webDriver, opens lostfilm page
in chrome webdriver, finds search line, sends
search request to it, and prints response data
in text format
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://www.lostfilm.tv/")
assert 'lostfilm' in driver.title.lower()
elem = driver.find_element_by_name("q")
elem.send_keys("galactica")
elem.send_keys(Keys.RETURN)
soup = BeautifulSoup(driver.page_source)
print(soup.get_text())
driver.close()