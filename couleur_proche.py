#Création d'une fonction qui cherche la couleur lego la plus proche

def couleurs_lego(lego_colors, searched_color):
  r, g, b = searched_color
  tab_color_diffs=[]
  for colors in lego_colors:
    Lr, Lg, Lb = colors
    difference_positive = (r - Lr)**2 + (g - Lg)**2 + (b - Lb)**2
    tab_color_diffs.append((difference_positive,colors))
  pluspetit=min(tab_color_diffs)
  return pluspetit[1]


def set_tab(color_settings): #Cette fonction définie l'ensemble des couleurs disponibles
  if color_settings == 0: # 0 correspond a noir et blanc
    lego_color=[(21,21,21),(244,244,244)]
  elif color_settings == 1: # 1 correspond a niveau de gris
    lego_color=[(21,21,21),(244,244,244),(66,66,62),(239,239,238),(230,237,207),(100,103,101),(160,161,159),(119,119,121),(135,141,143),(206,206,208)]
  else: #sinon c'est tt les couleurs
    lego_color=[(21,21,21),(244,244,244),(66,66,62),(239,239,238),(230,237,207),(100,103,101),(160,161,159),(119,119,121),(135,141,143),(206,206,208),(150,117,180),(188,166,208),(76,47,146),(118,114,181),(0,57,94),(0,108,183),(120,191,234),(0,153,212),(72,158,206),(132,200,226),(103,130,151),(0,163,218),(0,190,211),(24,158,159),(91,193,191),(193,228,218),(111,148,122),(0,74,45),(0,146,71),(0,175,77),(154,202,60),(204,225,151),(130,131,83),(0,168,79),(150,199,83),(227,224,41),(251,171,24),(255,205,3),(247,209,18),(255,245,121),(249,108,98),(240,87,41),(245,125,32),(245,136,48),(59,24,13),(105,46,20),(166,83,34),(175,116,70),(222,139,95),(252,195,158),(148,126,95),(151,137,108),(221,196,142),(127,19,27),(221,26,33),(229,30,38),(181,28,125),(232,80,156),(233,93,162),(246,173,205)]
  return lego_color