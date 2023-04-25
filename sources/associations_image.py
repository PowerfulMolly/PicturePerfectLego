import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
from resizeimage import resizeimage
from PIL import Image

def f_asso_image(nomimage,nomfond):

  img = Image.open(nomimage)
  img = img.convert("RGBA")
  fond = Image.open(nomfond)
  fond = fond.convert("RGBA")

  #Si le fond est plus petit que l'image, on cale l'image sur la taille du fond

  if img.size[0] > fond.size[0] or img.size[1] > fond.size[1]:

    largeur, hauteur = img.size
    HAUTEUR_IMAGES = fond.size[0]
    LARGEUR_IMAGES = fond.size[1]
    if hauteur >= HAUTEUR_IMAGES:
      ratio = HAUTEUR_IMAGES / hauteur
      img = img.resize((int(ratio * largeur), HAUTEUR_IMAGES), Image.LANCZOS)
    largeur, hauteur = img.size
    if largeur > LARGEUR_IMAGES:
      ratio = LARGEUR_IMAGES / largeur
      img = img.resize((LARGEUR_IMAGES, int(ratio * hauteur)), Image.LANCZOS)

  
  nvtaille = img.size #taille de l'image, pas du fond car on adapte le fond à l'image et pas l'invers
  width,height = img.size #valeur en pixel de la hauteur et de la largeur
  
  fond = resizeimage.resize_cover(fond,nvtaille)#fonction avec resizeimage pour rogner le fond pour qu'il soit à la taille de l'image
  
# en dessous, pour chaque pixel on verifie si il est transparent et si oui on change ce pixel par celui du fond 
  
  for x in range(width):
    for y in range(height):    
      T,H,K,A= img.getpixel((x, y)) 
      R,G,B,P= fond.getpixel((x,y))
      if A<=15: #Tolérance de 15 sur alpha
        img.putpixel((x,y),(R,G,B))
        
  img.save(dir_path+"/new_image.png")
  return()



def f_asso_color(nomimage,color_fond):

  img = Image.open(nomimage)
  img = img.convert("RGBA")

  (width,height) = img.size

  for x in range(width):
    for y in range(height):    
      T,H,K,A= img.getpixel((x, y))
      if A<=15: #Tolérance de 15 sur alpha
        img.putpixel((x,y),color_fond)
        
  img.save(dir_path+"/new_image.png")
  return()

