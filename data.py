from bs4 import BeautifulSoup

import requests

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def extract_data(url):
  response = requests.get(url)
  html = BeautifulSoup(response.content, 'html.parser')
  return html

html = extract_data(url)

print(html)
print(html.title)