from PIL import Image
import math as m
from couleur_proche import *
import for_transparent


def rognage_image(resolutionX, name_fichier):  # Fonction qui revoie une image rognée et la pixelisation a faire

  im = Image.open(name_fichier)
  (sizeX, sizeY) = im.size
  multiX = sizeX // resolutionX
  multiY = multiX
  if multiX > 1:
    #print("Les multiplicateurs en X et en Y sont : ", multiX, multiY)
    resolutionY = sizeY // multiY
    #print("La resolution est de", (resolutionX, resolutionY))

    new_tailleX = multiX * resolutionX
    new_tailleY = multiY * resolutionY
    surplusX = sizeX - new_tailleX
    surplusY = sizeY - new_tailleY

    if surplusX % 2 == 0:
      plusXG = surplusX // 2
      plusXD = surplusX // 2
    else:
      plusXG = (surplusX // 2) + 1
      plusXD = surplusX // 2

    if surplusY % 2 == 0:
      plusYG = surplusY // 2
      plusYD = surplusY // 2
    else:
      plusYG = (surplusY // 2) + 1
      plusYD = surplusY // 2
    #il n'y a pas de reste surplus=0
    #print((plusXG, plusXD), (plusYG, plusYD))

    new_img = Image.new("RGB", (new_tailleX, new_tailleY), (255, 255, 255))
    for Y in range(new_tailleY):
      for X in range(new_tailleX):
        (rouge, vert, bleu) = im.getpixel((X + plusXG, Y + plusYG))
        new_img.putpixel((X, Y), (rouge, vert, bleu))
    #new_img.save("image_rognée.jpg")
  else:
    new_img = im
    resolutionY = sizeY

  return new_img, multiX, name_fichier, resolutionY


def moyenne_des_pixels(
  x, y, tailleX, tailleY, im
):  #Création d'une fonction qui fait la moyenne des pixels avec en entrée les coordonnées et la taille
  (newR, newV, newB) = (0, 0, 0)
  for i in range(tailleX):
    for j in range(tailleY):
      (rouge, vert, bleu) = im.getpixel((x + i, y + j))
      (newR, newV, newB) = (newR + rouge, newV + vert, newB + bleu)
  (newR, newV,
   newB) = (newR // (tailleX * tailleY), newV // (tailleX * tailleY),
            newB // (tailleX * tailleY))
  return (newR, newV, newB)


def pixelisation(pixel, im, color_settings, name_fichier):
  memo_couleur = []
  (nbX, nbY) = im.size
  #print(im.size)
  tailleX = pixel
  tailleY = pixel
  carreX = nbX // pixel
  carreY = nbY // pixel
  resteX = nbX - carreX * pixel
  resteY = nbY - carreY * pixel
  #print(resteX, resteY)
  x = 0
  y = 0

  for f in range(carreY):
    for c in range(carreX):
      (R, V, B) = moyenne_des_pixels(x, y, tailleX, tailleY, im)
      (R, V, B) = couleurs_lego(set_tab(color_settings), (R, V, B))
      for d in range(tailleX):
        for e in range(tailleY):
          im.putpixel((x + d, y + e), (R, V, B))
      memo_couleur.append((R, V, B))
      x = x + pixel
    if resteX != 0:
      (R, V, B) = moyenne_des_pixels(x, y, resteX, tailleY, im)
      (R, V, B) = couleurs_lego(set_tab(color_settings), (R, V, B))
      for g in range(resteX):
        for j in range(tailleY):
          im.putpixel((x + g, y + j), (R, V, B))
      memo_couleur.append((R, V, B))
      x = 0
      y = y + pixel
    if resteX == 0:
      x = 0
      y = y + pixel
  for k in range(carreX):
    if resteY != 0:
      (R, V, B) = moyenne_des_pixels(x, y, tailleX, resteY, im)
      (R, V, B) = couleurs_lego(set_tab(color_settings), (R, V, B))
      for d in range(tailleX):
        for e in range(resteY):
          im.putpixel((x + d, y + e), (R, V, B))
      memo_couleur.append((R, V, B))
      x = x + pixel
  if resteX != 0 and resteY != 0:
    (R, V, B) = moyenne_des_pixels(x, y, resteX, resteY, im)
    (R, V, B) = couleurs_lego(set_tab(color_settings), (R, V, B))
    for d in range(resteX):
      for e in range(resteY):
        im.putpixel((x + d, y + e), (R, V, B))
    memo_couleur.append((R, V, B))

  nom = "./pixelised_image/pixel_{}_{}".format(pixel, name_fichier)   #C'est le nom de l'image pixelisée + son emplacement dans un fichier nommé "pixelised_image"
  im.save(nom)
  return memo_couleur, im


def pixelisation_for1(pixel, im, color_settings, name_fichier):

  (nbX, nbY) = im.size

  memo_couleur = []

  for x in range(nbX):
    for y in range(nbY):
      (R, V, B) = im.getpixel((x, y))
      (R, V, B) = couleurs_lego(set_tab(color_settings), (R, V, B))
      im.putpixel((x, y), (R, V, B))
      memo_couleur.append((R, V, B))
  nom = "pixel_{}_{}".format(pixel, name_fichier)
  #print(nom, "est été créé !")
  im.save(nom)
  return memo_couleur, im


def pixelisation_for_transparent(pixel, im, color_settings, name_fichier,
                                 remplacement):
  memo_couleur = []
  (nbX, nbY) = im.size
  #print(im.size)
  tailleX = pixel
  tailleY = pixel
  carreX = nbX // pixel
  carreY = nbY // pixel
  resteX = nbX - carreX * pixel
  resteY = nbY - carreY * pixel
  #print(resteX, resteY)
  x = 0
  y = 0

  for f in range(carreY):
    for c in range(carreX):
      (R, V, B) = moyenne_des_pixels(x, y, tailleX, tailleY, im)
      if (R, V, B) == (255, 255, 255):
        (R, V, B, A) = remplacement
      else:
        (R, V, B) = couleurs_lego(set_tab(color_settings), (R, V, B))
        A = 0
      for d in range(tailleX):
        for e in range(tailleY):
          im.putpixel((x + d, y + e), (R, V, B, A))
      memo_couleur.append((R, V, B, A))
      x = x + pixel

  nom = "pixel_transparent_{}_{}".format(pixel, name_fichier)
  #print(nom, "est été créé !")
  im.save(nom)
  return memo_couleur


def is_Transparent(name_fichier):
  im = Image.open(name_fichier)
  if len(im.getpixel((0, 0))) == 3:
    Transparent = False
  elif len(im.getpixel((0, 0))) == 4:
    Transparent = True
    #print(im.getpixel((0, 0)))
  return Transparent


'''#----------------------execution--------------------------

resolution = int(input("Quelle resolution voulez-vous appliquez a l'image (supérieure à 16, et de 16 puissance N) ?  "))
color_settings = 2

name_fichier = "fleur.png"

Transparent_remplacement=(255,255,255)

if is_Transparent(name_fichier) == False:
  img, nbpixel, name_fichier, resolutionY = rognage_image(resolution, name_fichier)
  is_Transparent=False
  if nbpixel <= 1:  # aucun changement
    memo_couleur = pixelisation_for1(nbpixel, img, color_settings,name_fichier)
  else:  # des changements
    memo_couleur = pixelisation(nbpixel, img, color_settings, name_fichier)

elif is_Transparent(name_fichier) == True:
  img, nbpixel, name_fichier, resolutionY = for_transparent.rognage_image(resolution, name_fichier)
  is_Transparent=True
  if nbpixel <= 1:  # aucun changement
    memo_couleur = for_transparent.pixelisation_for1_Transparent(nbpixel, img, color_settings, name_fichier, Transparent_remplacement)
  else:  # des changements
    memo_couleur = for_transparent.pixelisation_for_transparent(nbpixel, img, color_settings, name_fichier, Transparent_remplacement)

# on peut #print les différentes couleurs via : #print(memo_couleur)

#-------------Création de "pages"-------------

final_page = []

#16**2 = 256



resolutionX = resolution

multiX = nbpixel #multiX pixel originel = 1 gros pixel
multiY = multiX

#Il faut prendre dans le tableau

new_tailleX = multiX * resolutionX
new_tailleY = multiY * resolutionY

nb_fois = m.ceil(resolutionX / 16)

total_Y=resolutionY//16
nb_fois_Y=m.ceil(resolutionY / 16)
#print("nb_fois_Y = ", nb_fois_Y)
#print("total = ", total_Y)
reste_Y = resolutionY % 16

if reste_Y == 0 :
  reste_Y=16

taille_colonne=16

tab_16x16=[]

for y in range(nb_fois_Y):
  resolutionY=16
  if y==nb_fois_Y-1:
      resolutionY=reste_Y
  for h in range(nb_fois):
    name16x16="{}_{}_Image_16x16.png".format(h,y)
    indice = -1
    pages = []
    ind_16x16=-1 #réinitialisation
    image = Image.new('RGB', (784, 784), (255, 255, 255))
    for k in range(resolutionY):
      for i in range(0 + (16 *(y*taille_colonne*nb_fois)) + h * 16 + (16 * nb_fois * k), 16 + (16 *(y*taille_colonne*nb_fois)) + h * 16 + (16 * nb_fois * k)):  #Traitement par colonne
        if is_Transparent == True:
          (R, V, B, A) = memo_couleur[i]
        elif is_Transparent == False:
          (R, V, B) = memo_couleur[i]
        for pix2 in range(0 + (49*k), 49 + (49*k)):
          for pix in range(0 + 49*(i - (16 *(y*taille_colonne*nb_fois)) - h*16 - (16 * nb_fois * k)), 49 + 49*(i - (16 *(y*taille_colonne*nb_fois)) - h*16 - (16 * nb_fois * k))):
            image.putpixel((pix, pix2), (R, V, B)) #mettre les pixels
        ind_16x16+=1
        tab_16x16.append(memo_couleur[i])
        couleur = memo_couleur[i]
        find = False
        for a in pages: # Si il y est déjà on fait +1
          indice += 1
          if couleur == a[0]:
            find = True
            pages[indice][1] += 1
        indice = -1
        if find == False:
          pages.append([couleur, 1])
    image.save(name16x16, "PNG")
    final_page.append(pages)
  
#print("Opération finie ! ")
#print("len : ", len(final_page))
#print(nb_fois*nb_fois_Y)

#print("tab 16 fois 16 :", tab_16x16, "son len est : ", len(tab_16x16))

#memo_couleur a été vérifié

Image_tab=[]

#Construction en X
for y in range(nb_fois_Y):
  for h in range(nb_fois):
    nom_image="{}_{}_Image_16x16.png".format(h,y)
    Image_tab.append('<img id="image" src="{}"/>'.format(nom_image))
#print(Image_tab)

for I in range(len(final_page)):
  final_page[I].append(Image_tab[I])

#print("final page : ", final_page)

#Construction en Y
#for h in range(nb_fois):
#  for y in range(nb_fois_Y):
#    #print("{}_{}_Image_16x16.png".format(y,h))'''

  

        
'''#execution

resolution = int(input("Quelle resolution voulez-vous appliquez a l'image ? "))
color_settings = 2

img, nbpixel, name_fichier, Transparent = rognage_image(resolution, "SteamStore_VignetteA_01.png")

#print(Transparent)

if Transparent==False:
  #Teste pour multiX = 1 (ou multiX < 1)
  
  if nbpixel <= 1:
    memo_couleur = pixelisation_for1(nbpixel, img, color_settings, name_fichier)
  else:
    memo_couleur = pixelisation(nbpixel, img, color_settings, name_fichier)

else:
  memo_couleur = pixelisation_for_transparent(nbpixel, img, color_settings, name_fichier,(51,94,255,0))'''
