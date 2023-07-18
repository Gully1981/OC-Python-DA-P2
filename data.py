from bs4 import BeautifulSoup
import requests

#créer un loop pour scraper toutes les pages

#root est utile si le site ne mentionne pas les liens en absolu pour le concaténer
root = "http://books.toscrape.com"

#scraper tous les urls sur la page principale qu'on va scraper
response1 = requests.get(root)
urltxt = response1.text
soup1 = BeautifulSoup(urltxt, 'html.parser')


#récupérer les urls des catégories
category_links = []
main_categoryblock = soup1.find(class_="side_categories")
for category_link in main_categoryblock.select('a[href^="catalogue/category/books/"]'):
  href = category_link.get("href")
  category_links.append(href)


#scraper chaque page reprise dans la liste category_links qui reprend tous les liens des catégories récupérées dans la boucle précédente

books_in_category = []

for category_element in category_links:
    response = requests.get(f"{root}/{category_element}")
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    #mettre la variable dans la boucle pour qu'il récupère l'élément à chaque livre
    main_bookblock = soup1.find("section")
    sub_bookblock = main_bookblock.find_all("article", {"class": "product_pod"})

    # récupérer les urls des livres contenus dans chaque catégorie dans la boucle précédente
    for book_article in sub_bookblock:
      book_link = book_article.find("a")
      href = book_link.get("href")
      if href is not None:
        books_in_category.append(href)

#scraper chaque livre repris dans la boucle précédente
books_details =[]
for book_element in books_in_category:
  if book_element is not None:
    response2 = requests.get(f"{root}/{book_element}")
    content2 = response2.text
    soup2 = BeautifulSoup(content2, 'html.parser')

  # Récupérer les éléments dans chaque page de livre sur base des positions tableaux, classes etc
    #Définition des main elements pour récupérer les childs plus loin
    mainhighlight = soup2.find(class_="product_main")
    mainproductpage = soup2.find(class_="product_page")
    mainproductgallery = soup2.find("div", {"id": "product_gallery"})
    maintitlestring = mainhighlight.find("h1").string #ça peut aussi être .get_text() à la place de .string pour récupérer le texte

    #Récupérer la classse où est stockée la valeur d'étoiles données
    mainreview = soup2.find(class_="star-rating")
    if mainreview:
      #lister toutes les classes inclues dans mainreview
        classes = mainreview.get('class')
        #s'il y en a plus de 2
        if len(classes) >= 2:
          #pointer vers la 2e classe
            second_class = classes[1]
        else:
            second_class = "No review"

    #position du p dans la structure class product_page
    n = 1
    description = []
    for element in mainproductpage.select("p:nth-of-type("+str(n)+")"):
      #exclure le p qui est dans la div product_main en position 1 également
      if element not in mainhighlight:
       description.append(element.string)
      else:
        description.append("NA")

    #position des cellules d'un tableau
    maintable = soup2.find("table")
    #définir une variable pour récupérer tous les td du tableau
    maintd = soup2.find_all("td")

    #récupérer les éléments dans le tableau avec une boucle for pour les prendre 1 à 1
    tdupc = []
    for element_td in maintd:
      tdupc.append(element_td.string)

    # récupérer src image
    imagethumb = soup2.find_all("img")
    for source in imagethumb:
      imagesource = source["src"]

  books_details.append({
    "titre": maintitlestring,
    "description": description[0],
    "image url": imagesource,
    "upc": tdupc[0],
    "category": tdupc[1],
    "price excl": tdupc[3],
    "price incl": tdupc[4],
    "stock": tdupc[6],
    "review": second_class,
  })

#envoyer en csv

import csv

headers = ["titre","description","image url","upc","category","price excl","price incl","stock","review"]
rows = [maintitlestring, description[0], imagesource, tdupc[0],tdupc[1],tdupc[3],tdupc[4],tdupc[6],second_class]

with open("Devaux_Sandra_2_data_072023.csv", "w") as fichier:
  writer = csv.writer(fichier)
  #définit la ligne d'en-têtes
  writer.writerow(headers)

   #définit les lignes de contenu
  writer.writerow(rows)