
def pixelisation_execution(color_settings, resolution, name_fichier):
  from jinja2 import Template
  import main_pix
  import math as m
  from PIL import Image

  #--------------------------------------------------------------------EXECTUTION de la PIXELISATION--------------------------------------------------------------------


  Transparent_remplacement=(239,239,238) #De base le fond est Blanc couleur lego

  if main_pix.is_Transparent(name_fichier) == False:
    img, nbpixel, name_fichier, resolutionY = main_pix.rognage_image(resolution, name_fichier)
    is_Transparent=False
    if nbpixel <= 1:  # aucun changement
      memo_couleur, im = main_pix.pixelisation_for1(nbpixel, img, color_settings,name_fichier)
    else:  # des changements
      memo_couleur, im = main_pix.pixelisation(nbpixel, img, color_settings, name_fichier)

  elif main_pix.is_Transparent(name_fichier) == True:
    img, nbpixel, name_fichier, resolutionY = main_pix.for_transparent.rognage_image(resolution, name_fichier)
    is_Transparent=True
    if nbpixel <= 1:  # aucun changement
      memo_couleur = main_pix.for_transparent.pixelisation_for1_Transparent(nbpixel, img, color_settings, name_fichier, Transparent_remplacement)
    else:  # des changements
      memo_couleur = main_pix.for_transparent.pixelisation_for_transparent(nbpixel, img, color_settings, name_fichier, Transparent_remplacement)

  
  return nbpixel, resolution, resolutionY, memo_couleur, is_Transparent #Fin de la fonction


  #------------------------------- Fin de la fonction -------------------------


def f_inscructions(nb_pixel, resolution, resolutionY, memo_couleur, is_Transparent):

  from PIL import Image
  import webbrowser
  import math as m
  from jinja2 import Template
  import main_pix
  


  # Get File Content in String
  jinja2_template_string = open("template.html", 'r',newline='\n').read()

  # Create Template Object
  template = Template(jinja2_template_string)

  final_page = []

  resolutionX = resolution

  multiX = nb_pixel #multiX pixel originel = 1 gros pixel
  multiY = multiX

  #Il faut prendre dans le tableau

  new_tailleX = multiX * resolutionX
  new_tailleY = multiY * resolutionY

  nb_fois = m.ceil(resolutionX / 16)

  total_Y=resolutionY//16
  nb_fois_Y=m.ceil(resolutionY / 16)

  reste_Y = resolutionY % 16

  if reste_Y == 0 :
    reste_Y=16

  taille_colonne=16

  tab_16x16=[]

  tabimg_A_16x16=[] #Utile pour créer la tableau en haut à droite
  tabimg_B_16x16=[] #
  tabimg_C_16x16=[] #Utile pour créer le surlignage


  #Création de la liste total des pièces :
  liste_total =[]
  ind = -1
  find = False
  for h in range(len(memo_couleur)):
    if len(memo_couleur[h])==4:
      (R,V,B,A) = memo_couleur[h]
    elif len(memo_couleur[h])==3:
      (R,V,B) = memo_couleur[h]
    color = (R,V,B)
    for elem in liste_total: # Si il y est déjà on fait +1
      ind += 1
      if color == elem[0]:
          find = True
          liste_total[ind][1] += 1
    if find == False:
      liste_total.append([color, 1])
    ind=-1
    find = False

  def takeAmount(elem):
    return elem[1]

  liste_total.sort(key=takeAmount, reverse=True)

  #Création de la somme du total de pièce
  S=0
  for l in range(len(liste_total)):
    S=S+liste_total[l][-1]
    tab_Somme=[S]

  #Conversion des couleur en div
  for lego_color in liste_total:
    if len(lego_color[0])==3:
      R, V, B = lego_color[0]
    if len(lego_color[0])==4:
      R, V, B, A = lego_color[0]
    lego_color[0]="width:25px; height:25px; border:1px solid rgb({}, {}, {}); background-color: rgb({}, {}, {}); float: left; margin-right: 1em; border: 2px solid black;".format(R,V,B,R,V,B)
    lego_color[0]='style="{}">'.format(lego_color[0])

      



# Pour créer le tableau en haut à droite il faut savoir quel est le coté de plus grand

  plusgrand=0

  if nb_fois_Y > nb_fois:
    plusgrand=["Y", nb_fois_Y]
  else: # nb_fois => nb_fois_Y
    plusgrand=["X", nb_fois]


  # La taille du tableau étant de 360px
  # La taille d'un carré de 16x16 est de : X pixels
  #--------------------------------------------------------------------Création de la page web avec toutes les données + Des images en 16*16--------------------------------------------------------------------

  

  size16x16_pixel=int(360//plusgrand[1])

  plusgrand.append(size16x16_pixel)
      

  for y in range(nb_fois_Y):
    resolutionY=16
    if y==nb_fois_Y-1:
        resolutionY=reste_Y
    for h in range(nb_fois):
      name16x16="{}_{}_Image_16x16.png".format(h,y)
      name16x16_format='<a href="#{}"><img id="{}_image2" class="image2" src="./image_instructions/{}" style="width: {}px; height: {}px;"/></a>'.format(name16x16,name16x16,name16x16,size16x16_pixel,size16x16_pixel)
      tabimg_A_16x16.append(name16x16_format)
      tabimg_C_16x16.append(name16x16)
      indice = -1
      pages = []
      ind_16x16=-1 #réinitialisation
      image = Image.new('RGB', (784, 784), (255, 255, 255)) # ON PEUT CHANGER LA COULEUR DE FOND POUR LES PIXELS DONT ON A PAS BESOIN : ICI
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
      nom_avec_repertoire="./image_instructions/"+name16x16
      image.save(nom_avec_repertoire, "PNG")
      nom_image='<img class="image" id="{}" src="./image_instructions/{}"/>'.format(name16x16,name16x16)
      tabImage=[nom_image,'Image']
      pages.append(tabImage)
      final_page.append(pages)
    tabimg_B_16x16.append(tabimg_A_16x16)
    tabimg_A_16x16=[]

  for page in final_page:
      for couleur in page:
          if couleur[1]!='Image':
              if is_Transparent==False:
                R, V, B = couleur[0]
              if is_Transparent==True:
                R, V, B, A = couleur[0]
              couleur[0]="width:25px; height:25px; border:1px solid rgb({}, {}, {}); background-color: rgb({}, {}, {}); float: left; margin-right: 1em; border: 2px solid black;".format(R,V,B,R,V,B)
              couleur[0]='style="{}">'.format(couleur[0])


  #--------------------------------------------------------------------FIN DE L'EXECUTION--------------------------------------------------------------------


  #--------------------------------------------------------------------Création de la page web--------------------------------------------------------------------

  # Render HTML Template String
  html_template_string = template.render(pages = final_page, tableau_image = tabimg_B_16x16, test=tabimg_C_16x16, tableau_total_amount=liste_total, total_Lego=tab_Somme) #La variable test est utilisée pour le javascript en tant que liste des noms des images utilisées

  ##print(html_template_string)

  doc = open("Instructions.html","w",newline='\n')

  doc.write(html_template_string)

  #On ouvre le ficher html directememt

  webbrowser.open_new_tab('Instructions.html')

  return ()
