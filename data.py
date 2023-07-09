import csv

from bs4 import BeautifulSoup

import requests

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

#Extraire les données de l'url spécifique
def extract_data(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  return soup

soup = extract_data(url)

#Récupérer les éléments dans la page sur base des positions tableaux, classes etc
#Définition des main elements pour récupérer les childs plus loin
mainhighlight = soup.find(class_="product_main")
mainproductpage = soup.find(class_="product_page")
mainproductgallery = soup.find("div", {"id": "product_gallery"})


maintitlestring = mainhighlight.find("h1").string

#ça peut aussi être .get_text() à la place de .string pour récupérer le texte

#position du p dans la structure class product_page
n = 1
description = []
for element in mainproductpage.select("p:nth-of-type("+str(n)+")"):
  #exclure le p qui est dans la div product_main en position 1 également
  if element not in mainhighlight:
   description.append(element.string)

#position du p dans la structure class product_page
maintable = soup.find("table")

tdupc = []
#for element_upc in maintable.select("td:nth-of-type("+str(a)+")"):
for element_upc in maintable.select("td:nth-child(n+1)"):
  tdupc.append(element_upc.string)

# récupérer src image
imagethumb = soup.find_all("img")
for source in imagethumb:
  imagesource = source["src"]
#position des td dans la structure table et récupérer le contenu pour l'afficher
#n déjà défini plus haut


#Afficher les données dans le terminal
print(maintitle)
print(description)
print(imagesource)
print(tdupc)

#envoyer en csv

import csv

headers = ["titre","description","image url","upc","category","price excl","price incl","stock","review"]
rows = [maintitlestring, description, imagesource, tdupc]

with open("Devaux_Sandra_2_data_072023.csv", "w") as fichier:
  writer = csv.writer(fichier)
  #définit la ligne d'en-têtes
  writer.writerow(headers)

   #définit les lignes de contenu
  writer.writerow(rows)


  #essais

  # products = []
  # def get_allinfo_table(soup, products):
  # for table in soup.find_all("table"):
  #  for tr in table.find_all("tr")[1:]:
  #   td = tr.find_all("td")
  #  upc = td[0].get_text()
  #     product_type = td[1].get_text()
  #     price_excl = td[2].get_text()
  #     price_incl = td[3].get_text()
  #     stock = td[5].get_text()
  #     reviews = td[6].get_text()
  #     product = {
  #       "upc": upc,
  #       "product type": product_type,
  #       "prix excl": price_excl,
  #       "prix incl": price_incl,
  #       "stock": stock,
  #       "reviews": reviews
  #     }
  #     products.append(product)

#def load_data(soup,products):
 # headers = ["upc","product type","prix excl","prix incl","stock","review"]
  #with open(f"{title}.csv",mode="w", newline="") as file:
   # writer = csv.DictWriter(file, fieldnames=headers)
    #writer.writeheader()
    #for product in products:
     # writer.writerow(product)