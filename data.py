from bs4 import BeautifulSoup
import requests

#créer un loop pour scraper toutes les pages

#root est utile si le site ne mentionne pas les liens en absolu pour le concaténer
root = "http://books.toscrape.com"

#trouver tous les urls sur la page principale qu'on va scraper
#response1 = requests.get(root)
#urltxt = response1.text
#soup1 = BeautifulSoup(urltxt, 'html.parser')

#récupérer les url dans une variable links pour les réutiliser pour la prochaine boucle pour lire les données qui sont dedans
#for link in soup1.find_all("a"):
 # links = link.get("href")

#Pour scraper tous les liens contenus dans la page principale
#for links in link:
  #response = requests.get(f"{root}/{links}")
  #content = response.text
  #soup = BeautifulSoup(content, 'html.parser')

#Pour faire un scrape d'une page précise
response = requests.get("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
content = response.text
soup = BeautifulSoup(content, 'html.parser')

#Récupérer les éléments dans la page sur base des positions tableaux, classes etc
#Définition des main elements pour récupérer les childs plus loin
mainhighlight = soup.find(class_="product_main")
mainproductpage = soup.find(class_="product_page")
mainproductgallery = soup.find("div", {"id": "product_gallery"})
maintitlestring = mainhighlight.find("h1").string #ça peut aussi être .get_text() à la place de .string pour récupérer le texte

#position du p dans la structure class product_page
n = 1
description = []
for element in mainproductpage.select("p:nth-of-type("+str(n)+")"):
  #exclure le p qui est dans la div product_main en position 1 également
  if element not in mainhighlight:
   description.append(element.string)

#position du p dans la structure class product_page
maintable = soup.find("table")
maintd = soup.find("td")

#récupérer les éléments dans le tableau
tdupc = []
for element_upc in maintd.contents:
  tdupc.append(element_upc.string)

# récupérer src image
imagethumb = soup.find_all("img")
for source in imagethumb:
  imagesource = source["src"]
#position des td dans la structure table et récupérer le contenu pour l'afficher
#n déjà défini plus haut


#Afficher les données dans le terminal
print(maintitlestring)
print(description)
print(imagesource)
print(tdupc)
#print(links)

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