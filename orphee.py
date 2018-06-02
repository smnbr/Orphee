from tkinter import *
from tkinter import filedialog
import time, pygame.mixer, pygame.sndarray, samplerate, random
import PIL.Image, PIL.ImageTk
from math import *


#fonction choisir un fichier
def selectimage():
    global filename
    global select
    filename = filedialog.askopenfilename(initialdir="~/",title="Selectionnez une image",filetypes=(("fichier jpg",'*.jpg'),("fichier jpeg",'*.jpeg'),("fichier png",'*.png')))
    if filename != "":
        select = Label(fenetre, text="Image sélectionnée", bg = "#a7c1de")
        select.pack(pady=20)
    
#fonction tableau avec des valeurs de 0.5 à 1.5 en fonction des couleurs des pixels
def imgarray(filename):
    with PIL.Image.open(filename) as img:
        width, height = img.size
    
    #calcul nombre total de pixels
    width = int(width)
    height = int(height)
    totalpixels=width*height

    #nombre de pixels à analyser (arr. inf)
    touslesxpixels=floor(totalpixels/42)

    #ouvir l'image avec PIL
    im = PIL.Image.open(filename, 'r')

    #toutes les valeurs RGB de l'image
    pix_val = list(im.getdata())

    #sélection des données nécessaires (pour qu'il y en ait 42 en tout)
    listecouleurspixels= [0]*42
    for i in range (42) :
        selection = pix_val[touslesxpixels*i]
        listecouleurspixels[i] = selection

    pix_val_flat = [x for sets in listecouleurspixels for x in sets]

    n = 0
    compteur = 0
    valeursfiniespixels = [0]*42

    for i in range (42) :
        valtot = 0
        for z in range (3) :
            valtot += pix_val_flat[n]
            n+=1
        valeurdeci = valtot/765 + 0.5
        valeursfiniespixels[i] = valeurdeci
    return valeursfiniespixels


def playson(tabson, ratio):
    # resampler pour augmenter la fréquence du son et donc le pitcher
    resampleson = samplerate.resample(tabson, ratio, "sinc_fastest").astype(tabson.dtype)
    
    # jouer le son obtenue
    sortie = pygame.sndarray.make_sound(resampleson)
    sortie.play()

def start(filename, optionlist):
    #ouvrir nouvelle fenetre avec l'image
    fenetreimage = Toplevel()
    fenetreimage.resizable(False,False)

    #conversion image pour pouvoir l'utiliser
    imgpil = PIL.Image.open(filename)
    bgimage = PIL.ImageTk.PhotoImage(imgpil)

    #création canvas
    largeur = bgimage.width()
    hauteur = bgimage.height()
    canvas = Canvas(fenetreimage, width = largeur-5, height = hauteur-5, bg = 'black')
    canvas.pack()
    canvas.create_image(0, 0, image = bgimage, anchor= NW)
    fenetreimage.update()
    
    # récupérer le fichier son correspondant
    choixinstru=var.get()
    son = pygame.mixer.Sound(optionlist[choixinstru])
    
    # charger le son dans un tableau en fonction des fréquences
    tabson = pygame.sndarray.array(son)
    valeursfiniespixels = imgarray(filename)
    for i in valeursfiniespixels:
        playson(tabson, i)
        time.sleep(random.uniform(0.20, 0.20))

    #fermer fenetreimage et indicateur de sélection
    select.destroy()
    fenetreimage.destroy()

#configuration fenetre TKinter
fenetre = Tk()
fenetre.configure(bg="#1B4D7C")
fenetre.geometry('900x640')
fenetre.title("Orphée - Projet d'ISN")

label=Label(fenetre, text="Orphée", font=("Arial", 44), bg = "#a7c1de").pack(side="top", pady=30)      
label2 = Label(fenetre, text= "Projet d'ISN - 2017-2018 - Professeur : M. Elophe", font=("Arial", 22), bg="#a7c1de").pack(side=BOTTOM, padx=5, pady=20)
img_fond_pil = PIL.Image.open('ressources/orphee_fond.png')

img_fond_pil = img_fond_pil.resize((290, 169), PIL.Image.ANTIALIAS)
img_fond = PIL.ImageTk.PhotoImage(img_fond_pil)
labelimg = Label(fenetre, image=img_fond, borderwidth=0).pack()

global var
optionlist = {"Piano":"ressources/piano.wav", "Violon":"ressources/violon.wav", "Guitare":"ressources/guitare.wav"}
var = StringVar(fenetre)
var.set("Piano")
option = OptionMenu(fenetre, var, "Piano", "Violon", "Guitare")
option["bg"] = "#1B4D7C"
option.pack(pady=20)




#bouton activant fonction selectimage
filename =""
boutonfichier = Button(fenetre, text="Choisir une image", command=selectimage, highlightbackground= "#1B4D7C")
boutonfichier.pack(pady=20)

#initiation du module pygame
pygame.mixer.init(44100,-16,2,4096)

boutondebut = Button(fenetre, text="Démarrer", command=lambda:start(filename, optionlist), highlightbackground= "#1B4D7C").pack(pady=20)

