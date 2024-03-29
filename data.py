from bs4 import BeautifulSoup
import requests
#initialiser import csv pour avoir 1 csv par catégorie avant de démarrer le loop des livres
import csv
#parser l'url pour récupérer une partie précise
from urllib.parse import urlparse
# permettre la lecture des url pour télécharger les images des livres
import urllib.request
#gestion des erreurs en cas d'urls 404
import urllib.error
# permettre la création de folders par catégorie pour stocker les images
import os
#nettoyer les alt des images pour supprimer les accents et autres caractères spéciaux qui bloquent le download des images
import re

##créer un loop pour scraper toutes les pages

#root est utile si le site ne mentionne pas les liens en absolu pour le concaténer
root = "https://books.toscrape.com"

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

    #Pour récupérer la catégorie seule dans l'url repris dans category_element - nécessaire pour le nom du fichier csv par cat.
    parsed_url = urlparse(category_element)
    category_name = parsed_url.path.split("/")[-2]

    #créer un folder par catégorie pour stocker les images (import os fait avant d'entrer dans cette boucle)
    folder_name = f"images/{category_name}"
    os.makedirs(folder_name, exist_ok=True)

    #trouver les paginations pour avoir le nombre total de pages à scraper + if condition pour ne pas appliquer s'il n'y en a pas
    num_pages = 1
    pagination = soup.find("a", string="next")
    if pagination:
      page_url = pagination["href"]
      page_number = int(page_url.split("-")[1].split(".")[0])
      num_pages = page_number

    #ajouter les pages de la pagination dans le loop
    for page in range(1, num_pages + 1):
      page_url = f"{root}/{category_element}/page-{page}.html"
      response = requests.get(page_url)
      content = response.text
      soup = BeautifulSoup(content, "html.parser")

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

        #récupérer la catégorie
        mainlinks = soup2.find("ul", class_= "breadcrumb")
        bookcategory = mainlinks.contents[5].get_text(strip=True)


        # récupérer src image
        imagethumb = soup2.find_all("img")

        for source in imagethumb:
          imagesource = source["src"]

          #télécharger les images
           #récupérer l'url absolu
          imageshorturl = imagesource.replace("../../", "")
          image_urlabsolu = f"{root}/{imageshorturl}"
           #pour renommer l'image avec l'alt en supprimant les espaces
          image_alt = source.get("alt","").replace(" ","")
          def sanitize_image_alt(image_alt):
            #supprimer les caractères spéciaux avec import re
            return re.sub(r"[^\w\-_\.\']","_", image_alt)
          #définir le path de chaque image par le nom du dossier par catégorie défini plus haut + nom image
          image_path = os.path.join(folder_name, f"{image_alt}.jpg")
           #pour enregistrer l'image
          response4 = urllib.request.urlopen(image_urlabsolu)
          with open(image_path, "wb") as f:
              f.write(response4.read())

      books_details.append({
        "titre": maintitlestring,
        "description": description[1],
        "image url": imagesource,
        "upc": tdupc[0],
        "category": bookcategory,
        "price excl": tdupc[2],
        "price incl": tdupc[3],
        "stock": tdupc[5],
        "review": second_class,
      })

    headers = ["titre","description","image url","upc","category","price excl","price incl","stock","review"]

    with open(f"Devaux_Sandra_2_data_072023_{category_name}.csv", "w") as fichier:
      writer = csv.writer(fichier)
      #définit la ligne d'en-têtes
      writer.writerow(headers)

      #sortir tous les éléments des livres avec 1 par ligne en appelant la valeur 1 définie pour chaque élément dans le dictionnaire books_details
      for book_details in books_details:
        rows = [
          book_details["titre"],
          book_details["description"],
          book_details["image url"],
          book_details["upc"],
          book_details["category"],
          book_details["price excl"],
          book_details["price incl"],
          book_details["stock"],
          book_details["review"],
        ]
        #définit les lignes de contenu
        writer.writerow(rows)

