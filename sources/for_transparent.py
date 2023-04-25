import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
from PIL import Image
import math as m
from couleur_proche import *

def rognage_image(resolutionX, name_fichier):  # Fonction qui revoie une image rognée et la pixelisation a faire

  im = Image.open(name_fichier)
  (sizeX, sizeY) = im.size
  multiX = sizeX // resolutionX
  multiY = multiX
  if multiX >= 1:
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

    new_img = Image.new("RGBA", (new_tailleX, new_tailleY), (255, 255, 255,0))
    for Y in range(new_tailleY):
      for X in range(new_tailleX):
        (rouge, vert, bleu, alpha) = im.getpixel((X + plusXG, Y + plusYG))
        new_img.putpixel((X, Y), (rouge, vert, bleu, alpha))
  else:
    new_img = im
    resolutionY = sizeY

  return new_img, multiX, name_fichier, resolutionY


def pixelisation_for_transparent(pixel, im, color_settings, name_fichier, remplacement):
  memo_couleur=[]
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

  (R_remp, V_remp, B_remp) = remplacement
  

  for f in range(carreY):
    for c in range(carreX):
      (R, V, B, A) = moyenne_des_pixels_for_Transparent(x, y, tailleX, tailleY, im)
      if A == 0:
        (R, V, B, A) = (R_remp, V_remp, B_remp,255)
      else:
        (R, V, B) = couleurs_lego(set_tab(color_settings), (R, V, B))
        A=255
      for d in range(tailleX):
        for e in range(tailleY):
          im.putpixel((x + d, y + e), (R, V, B, A))
      memo_couleur.append((R,V,B,A))
      x = x + pixel
    y = y + pixel
    x=0

  print(dir_path)
  nom = dir_path+"/pixelised_image/pixel_{}_{}".format(pixel, name_fichier)   #C'est le nom de l'image pixelisée + son emplacement dans un fichier nommé "pixelised_image"
  im.save(nom)
  return memo_couleur


def moyenne_des_pixels_for_Transparent(
  x, y, tailleX, tailleY, im
):  #Création d'une fonction qui fait la moyenne des pixels avec en entrée les coordonnées et la taille
  (newR, newV, newB, newA) = (0, 0, 0, 0)
  for i in range(tailleX):
    for j in range(tailleY):
      (rouge, vert, bleu, alpha) = im.getpixel((x + i, y + j))
      (newR, newV, newB, newA) = (newR + rouge, newV + vert, newB + bleu, newA + alpha)
  (newR, newV,
   newB, newA) = (newR // (tailleX * tailleY), newV // (tailleX * tailleY),
            newB // (tailleX * tailleY), newA // (tailleX * tailleY))
  return (newR, newV, newB, newA)

def pixelisation_for1_Transparent(pixel, im, color_settings, name_fichier, remplacement):

  (nbX, nbY) = im.size

  for x in range(nbX):
    for y in range(nbY):
      (R, V, B, A) = im.getpixel((x, y))
      (R, V, B) = couleurs_lego(set_tab(color_settings), (R, V, B))
      A=0
      im.putpixel((x, y), (R, V, B, A))
  nom = "pixel_{}_{}".format(pixel, name_fichier)
  #print(nom, "est été créé !")
  im.save(dir_path+'/'+nom)
  return


'''#execution

resolution = int(input("Quelle resolution voulez-vous appliquez a l'image ? "))
color_settings = 2

img, nbpixel, name_fichier = rognage_image(resolution, "SteamStore_VignetteA_01.png")

#Teste pour multiX = 1 (ou multiX < 1)

if nbpixel <= 1:
    memo_couleur = pixelisation_for1_Transparent(nbpixel, img, color_settings, name_fichier)
else:
  memo_couleur = pixelisation_for_transparent(nbpixel, img, color_settings, name_fichier)'''
