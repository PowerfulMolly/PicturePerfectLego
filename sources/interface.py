from tkinter import *
from tkinter.messagebox import *  # Pour utiliser les alertes de notre os
from tkinter import filedialog
from PIL import Image, ImageTk
import math as m

LARGEUR_IMAGES = 500 #Ces chiffres sont le nombre de pixels maximums pour afficher l'image sur l'interface tkinter en abcisse et en ordonéees
HAUTEUR_IMAGES = 350


def cropImage(img): #Cette fontion permet de donner une nouvelle taille à une image en fonction de la taille maximale donnée précédement
  largeur, hauteur = img.size
  if hauteur >= HAUTEUR_IMAGES:
    ratio = HAUTEUR_IMAGES / hauteur
    img = img.resize((int(ratio * largeur), HAUTEUR_IMAGES), Image.LANCZOS)
  largeur, hauteur = img.size
  if largeur > LARGEUR_IMAGES:
    ratio = LARGEUR_IMAGES / largeur
    img = img.resize((LARGEUR_IMAGES, int(ratio * hauteur)), Image.LANCZOS)
  return img

#--------------------------------------------------Création de la fenêtre tkinter--------------------------------------------------#

fenetre = Tk() 

couleur_fenetre = '#ABABAB' #Couleur de la fenêtre

fenetre['bg'] = couleur_fenetre #Application de la couleur en fond

fenetre.geometry("1400x800") #Taille de la fenêtre

fenetre.title('PicturePerfectLego') #Ceci est le titre de la fenêtre

#--------------------------------------------------Affichage du logo (En haut à gauche)--------------------------------------------------#

image_logo = PhotoImage(file="./Logo.png")

canvas = Canvas(fenetre,width=100, height=100)
canvas.create_image(0, 0, anchor=NW, image=image_logo)
canvas.pack(side = TOP, anchor = NW)

#Création d'une frame (d'un cadre) qui comprend toute la taille de la fenêtre principale

frame = Frame(fenetre, bg=couleur_fenetre)
frame.pack()

#Création d'une frame (d'un cadre) pour le titre

frame_titre = Frame(frame, borderwidth=5,bg=couleur_fenetre) 
frame_titre.pack(side=TOP, padx=0, pady=0)

#Création d'une frame (d'un cadre) pour le côté droit

right_frame = Frame(frame, width=540, borderwidth=5, bg=couleur_fenetre)
right_frame.pack(side=RIGHT, anchor="w", padx=0, pady=10)

#Création d'une frame (d'un cadre) pour le côté gauche

left_frame = Frame(frame, width=540, borderwidth=5, bg=couleur_fenetre)
left_frame.pack(side=LEFT, padx=0, pady=0, expand=False)

#--------------------------------------------------Cette fonction indique si l'image donnée en paramètre est transparente--------------------------------------------------#

def image_transparent(im): 
  (s_X,s_Y)=im.size
  Transparent = False
  if len(im.getpixel((0, 0))) == 4:
    for i in range(s_X):
      for j in range(s_Y):
        (R, V, B, A) = im.getpixel((i, j))
        if A == 0:
          Transparent = True

  return Transparent

#---Cette fonction est exécutée quand on a appuyé sur le bouton "Appuyer pour mettre une image" : elle donne une taille correcte à l'image et appelle un autre fonction qui fait la pixelisation dans le fichier "Main_programme"---#

def f_image():

  global filename
  
  button.configure(state="disabled") #On déactive le bouton "Appuyer pour mettre une image" temporairement
  filename = 'None'
  filename = filedialog.askopenfilename(initialdir="/", title="Selectionnez un fichier",filetypes=(("png files", "*.png"),("jpg files", "*.jpg"),("all files", "*.*")))

  #Utilisation de "filedialog.askopenfilename" permet de demander à l'utilisateur une image dans ses fichiers

  im = Image.open(filename)

  resized_image = cropImage(im) #On donne une nouvelle taille à l'image de l'utilisateur via une nouvelle image nommée "resized_image"

  #On cherche le nom de l'extention de l'image de l'utilisateur (.png ou .jpg)
  extention_tab = filename.split(".")
  extention = extention_tab[-1]

  global nom_resized
  nom_resized = 'resized_image.' + extention
  resized_image.save(nom_resized) # On sauvegarde la nouvelle image nommée "resized_image" avec la bonne extension

  if image_transparent(resized_image) == True: # Un nouvleau paramètre apparait si l'image a des pixels transparents
    

    global label_transparent
    label_transparent=Label(right_frame, borderwidth=3, font=('Helvetica 15 underline'), bg=couleur_fenetre, text="Fond personnalisé pour l'image" + '\n') #On crée un titre "Fond pour l'image transparente"
    label_transparent.grid(padx=2,row=6,column=1)

    f1_v = StringVar()
    f1_v.set('None')
    global fond1
    fond1 = Radiobutton(right_frame, #On crée un choix entre deux de boutons nommé "fond1" et "fond2"
                       text='Utiliser une image de fond',
                       bg=couleur_fenetre,
                       variable=f1_v,
                       value='Image',
                       command=lambda: f_update2('Image'))
    fond1.grid(row=7, column=1)

    global fond2
    fond2 = Radiobutton(right_frame,
                       text='Utiliser une couleur de fond',
                       bg=couleur_fenetre,
                       variable=f1_v,
                       value='Couleur',
                       command=lambda: f_update2('Couleur'))
    fond2.grid(row=7, column=3)

    global button_fond
    button_fond = Button(right_frame, font='Arial',text="Appuyez pour instaurer un fond à l'image", command=lambda: f_fond())
    button_fond.grid(row=8,column=2, pady=15)


  (maxSizeX, maxSizeY) = resized_image.size

  global maxResolution
  maxResolution = m.floor(maxSizeX / 16) // 2  #On défini le niveau maximum de resolution (correspond à k*16) et on divise par 2 pour ne pas avoir a rendre une image qui à la même résolution qu'avant
  
  #On affiche la nouvelle image "resized_image" dans l'interface
  new_image = ImageTk.PhotoImage(resized_image)
  global labelImage_debut   # On retrouve a plusieurs reprise la fonction "global" : elle est utilisée pour pouvoir utiliser les différentes variables dans d'autres fonctions 
  labelImage_debut = Label(left_frame,image=new_image,bd=0,highlightthickness=0)
  labelImage_debut.grid(row=1, column=0)

  global button_pixelisation  #On a besoin d'utiliser global pour pouvoir utiliser "button_pixelisation" dans d'autres fonctions

  button_pixelisation = Button(left_frame,
                               font='Arial',
                               text="Appuyez pour pixeliser",
                               command=lambda: IMAGE_pixelisation())
  button_pixelisation.grid(row=2, column=0, pady=2) #On crée le bouton qui déclenche la pixelisation

  #-----------------------------Création d'un croix à droite de l'image pour pouvoir revenir en arrière-----------------------------#
  image_croix = PhotoImage(file="croix_50x50.png")

  global Croix1

  Croix1 = Button(left_frame,
                  bg=couleur_fenetre,
                  image=image_croix,
                  bd=0,
                  highlightthickness=0,
                  command=f_undo_image1)
  Croix1.grid(row=1, column=1)

  #Création du curseur du niveau de Résolution & du titre "Resolution de l'image installée"

  global label_resloution
  label_resloution=Label(right_frame,borderwidth=3,font=('Helvetica 15 underline'),bg=couleur_fenetre,text="Resolution de l'image installée" + '\n')
  label_resloution.grid(padx=2, row=4, column=1)  #Création du titre de la résolution

  global curseur2
  curseur2 = Scale(right_frame,
                   orient='horizontal',
                   from_=1,
                   to=maxResolution,
                   tickinterval=4,
                   length=400,
                   label="Niveau de Résolution a appliquer à l'image")
  curseur2.grid(row=5, column=2)

  fenetre.mainloop()

  return

def f_fond(): #Cette fonction est activée quand il faut mettre une image de fond ou une couleur

  if fond=='Image':
    nom_fond=filedialog.askopenfilename(initialdir="/", title="Selectionnez un fichier non transparent",filetypes=(("png files", "*.png"),("jpg files", "*.jpg"),("all files", "*.*")))
    import associations_image
    associations_image.f_asso_image(nom_resized, nom_fond) #On ajoute l'image donnée par l'utilisateur au fond

    button.configure(state="disabled")

    labelImage_debut.destroy()

    label_transparent.destroy() #On détruit le titre "Fond pour l'image transparente"

    fond1.destroy()
    fond2.destroy()
    button_fond.destroy()

    if button_pixelisation['state'] == DISABLED:

      button_pixelisation.destroy()

      labelImage_fin.destroy()

      button_instructions.destroy()

      Croix2.destroy()

    else:
      button_pixelisation.destroy()

    Croix1.destroy()

    f_fond2()

  elif fond=='Couleur':
    global newWindow
    newWindow = Toplevel(fenetre)
    newWindow.title("Choisir la couleur de fond")
    newWindow.geometry("400x200")
    Label(newWindow,text ="Choisissez la couleur de fond pour votre image").pack()

    #Création du choix de couleur

    choices = ['Noir','Gris','Rouge Foncé','Rouge','Orange','Marron','Jaune','Vert Foncé','Vert','Bleu Foncé','Bleu','Rose','Violet','Blanc']
    global variable
    variable = StringVar(newWindow)
    variable.set('Rouge')
    w = OptionMenu(newWindow, variable, *choices)
    w.pack()
    bouton_vad_color=Button(newWindow,font='Arial',text="Valider la couleur",command=lambda: validation_couleur())
    bouton_vad_color.pack() #On crée le bouton qui valide la couleur de fond
    newWindow.mainloop()

  
  return


def f_fond2(): #C'est une fonction qui suprime l'image précédente pour mettre l'image avec son nouveau fond
  
  #On réaffiche l'image
  global nom_resized
  nom_resized = 'new_image.png'
  resized_image = Image.open(nom_resized)

  (maxSizeX, maxSizeY) = resized_image.size


  global maxResolution
  maxResolution=m.floor(maxSizeX/16)//2 #Pour ne pas être a du 1 pixel pour 1 pixel


  new_image=ImageTk.PhotoImage(resized_image)

  global labelImage_debut

  labelImage_debut = Label(left_frame, image=new_image,bd=0,highlightthickness=0)
  labelImage_debut.grid(row=1,column=0)

  global button_pixelisation #On a besoin d'utilier global pour pouvoir utiliser "button_pixelisation" dans d'autres fonctions

  button_pixelisation = Button(left_frame, font='Arial',text="Appuyez pour pixeliser", command=lambda: IMAGE_pixelisation())
  button_pixelisation.grid(row=2,column=0, pady=2)

  #CREATION DE LA PREMIERE CROIX -----------------------------

  image_croix = PhotoImage(file="croix_50x50.png")

  global Croix1

  Croix1 = Button(left_frame, bg=couleur_fenetre, image = image_croix, bd=0,highlightthickness=0, command=f_undo_image1)
  Croix1.grid(row=1,column=1)



  #Création du curseur du niveau de Résolution & du titre "Resolution de l'image installée"

  global label_resloution
  label_resloution=Label(right_frame,borderwidth=3,font=('Helvetica 15 underline'),bg=couleur_fenetre,text="Resolution de l'image installée" + '\n')
  label_resloution.grid(padx=2, row=4, column=1)  #Création du titre de la résolution

  global curseur2
  curseur2 = Scale(right_frame, orient='horizontal', from_=1,to=maxResolution, tickinterval=4,length=400,label="Niveau de Résolution a appliquer à l'image")
  curseur2.grid(row=5,column=2)

  fenetre.mainloop()

  return

#Création de la fonction d'update du choix de couleur


select_color = 2 #On défini select_color à 2 pour être sur

def f_update(): #Cette fonction enregistre le choix entre toutes les couleurs, niveau de gris, et noir & blanc
  global select_color
  valeur = r1_v.get()
  if valeur == 'All':
    select_color = 2
  if valeur == 'Niv_gray':
    select_color = 1
  if valeur == 'Black_white':
    select_color = 0
  return ()


def f_update2(valeur): #Cette fonction enregistre le choix entre couleur ou image de fond
  global fond
  if valeur=='Image':
    fond='Image'
  if valeur=='Couleur':
    fond='Couleur'
  return ()


def validation_couleur(): # Cette fonction valide la couleur de fond
  global Transparent_remplacement
  if variable.get() == 'Noir':
    Transparent_remplacement=(0,0,0,255)
  if variable.get() == 'Gris':
    Transparent_remplacement=(165,165,165,255)
  if variable.get() == 'Rouge Foncé':
    Transparent_remplacement=(137,0,0,255)
  if variable.get() == 'Rouge':
    Transparent_remplacement=(246,6,6,255)
  if variable.get() == 'Orange':
    Transparent_remplacement=(235,160,19,255)
  if variable.get() == 'Marron':
    Transparent_remplacement=(139,69,19,255)
  if variable.get() == 'Jaune':
    Transparent_remplacement=(255,255,0,255)
  if variable.get() == 'Vert Foncé':
    Transparent_remplacement=(0,100,0,255)
  if variable.get() == 'Vert':
    Transparent_remplacement=(34,139,34,255)
  if variable.get() == 'Bleu Foncé':
    Transparent_remplacement=(0,0,139,255)
  if variable.get() == 'Bleu':
    Transparent_remplacement=(65,105,225,255)
  if variable.get() == 'Rose':
    Transparent_remplacement=(255,0,255,255)
  if variable.get() == 'Violet':
    Transparent_remplacement=(128,0,128,255)
  if variable.get() == 'Blanc':
    Transparent_remplacement=(0,0,0,255)

  import associations_image
  associations_image.f_asso_color(nom_resized,Transparent_remplacement)

  button.configure(state="disabled")

  labelImage_debut.destroy()

  label_transparent.destroy() #On détruit le titre "Fond pour l'image transparente"

  fond1.destroy()
  fond2.destroy()
  button_fond.destroy()

  if button_pixelisation['state'] == DISABLED:

    button_pixelisation.destroy()

    labelImage_fin.destroy()

    button_instructions.destroy()

    Croix2.destroy()

  else:
    button_pixelisation.destroy()

  Croix1.destroy()

  newWindow.destroy()

  f_fond2()
  
  return


def f_undo_image1():

  button.configure(state="normal")

  labelImage_debut.destroy()

  if button_pixelisation['state'] == DISABLED:

    button_pixelisation.destroy()

    labelImage_fin.destroy()

    button_instructions.destroy()

    Croix2.destroy()

  else:
    button_pixelisation.destroy()

  Croix1.destroy()

  return


def f_undo_image2():

  button_pixelisation.configure(state="normal")

  labelImage_fin.destroy()

  button_instructions.destroy()

  Croix2.destroy()

  return


Label(right_frame,
      font=("Arial", 18),
      bg=couleur_fenetre,
      text="Parametres").grid(padx=2, row=1, column=2)

Label(frame_titre,
      font=('Helvetica 32 underline'),
      bg=couleur_fenetre,
      text="Bienvenue sur PicturePerfectLego").grid()

button = Button(left_frame,
                font='Arial',
                text="Appuyez pour téléverser une image",
                command=f_image)
button.grid(
  row=0, column=0, pady=2
)


#Création du choix de couleur

r1_v = StringVar()
r1_v.set('All')

Label(right_frame,
      borderwidth=3,
      font=('Helvetica 15 underline'),
      bg=couleur_fenetre,
      text="Couleur à utiliser..." + '\n').grid(
        padx=2, row=2, column=1)  #Création du titre des couleurs

couleur1 = Radiobutton(right_frame,
                       text='Toutes les couleurs',
                       bg=couleur_fenetre,
                       variable=r1_v,
                       value='All',
                       command=f_update)
couleur1.grid(row=3, column=1)

couleur2 = Radiobutton(right_frame,
                       text='Niveau de Gris',
                       bg=couleur_fenetre,
                       variable=r1_v,
                       value='Niv_gray',
                       command=f_update)
couleur2.grid(row=3, column=2)

couleur3 = Radiobutton(right_frame,
                       text='Noir et Blanc',
                       bg=couleur_fenetre,
                       variable=r1_v,
                       value='Black_white',
                       command=f_update)
couleur3.grid(row=3, column=3)

#Le niveau de Résolution est créé après car il faut connaitre la résolution maximum


global resolution #On défini resolution à 16 pour être sur
resolution = 16

global Transparent_remplacement
Transparent_remplacement = (239,239,238) #Blanc couleur lego


def IMAGE_pixelisation():

  button_pixelisation.configure(
    state="disabled")  # Le bouton pour pixeliser est désactivé

  import Main_programme

  resolution = curseur2.get() * 16

  if resolution == 0:
    resolution = 16

  #print('select_color = ', select_color)
  #print('resolution = ', resolution)
  #print('nom_resized = ', nom_resized)

  global nb_pixel, resolution_X, resolution_Y, memo_couleur, is_Transparent
  nb_pixel, resolution_X, resolution_Y, memo_couleur, is_Transparent = Main_programme.pixelisation_execution(select_color, resolution, nom_resized)

  img = Image.open(nom_resized)

  (sizeAb, sizeOrd) = img.size

  pixel = sizeAb // resolution

  nom_pixelised = "./pixelised_image/pixel_{}_{}".format(pixel, nom_resized) #C'est le nom de l'image pixelisée + son emplacement dans un fichier nommé "pixelised_image"


  image_pixelised = ImageTk.PhotoImage(file=nom_pixelised)

  global labelImage_fin

  labelImage_fin = Label(left_frame,
                         image=image_pixelised,
                         bd=0,
                         highlightthickness=0)

  labelImage_fin.grid(row=3, column=0) 

  #Création du bouton pour créer les instructions-----------------------------------

  global button_instructions  #On a besoin d'utilier global pour pouvoir utiliser "button_instructions" dans d'autres fonctions

  button_instructions = Button(left_frame,
                               font='Arial',
                               text="Appuyez pour obtenir les intructions (L'opération peut être longue)",
                               command=lambda: f_launch_pixelisation())
  button_instructions.grid(row=4, column=0, pady=2)  

  #CREATION DE LA DEUXIEME CROIX-----------------------------

  image_croix = PhotoImage(file="croix_50x50.png")

  global Croix2

  Croix2 = Button(left_frame,
                  bg=couleur_fenetre,
                  image=image_croix,
                  bd=0,
                  highlightthickness=0,
                  command=f_undo_image2)
  Croix2.grid(row=3, column=1)

  fenetre.mainloop()

  return


def f_launch_pixelisation():

  button_instructions.configure(
    state="disabled")  # Le bouton pour les instructions est désactivé

  import Main_programme

  Main_programme.f_inscructions(nb_pixel, resolution_X, resolution_Y,
                                memo_couleur, is_Transparent)

  return


fenetre.mainloop()  # démarrage du réceptionnaire d’événements

#fenetre.destroy()  # destruction (fermeture) de la fenêtre
