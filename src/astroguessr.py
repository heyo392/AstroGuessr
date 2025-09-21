import pandas as pd
import tkinter as tk
import numpy as np
from math import pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.text import Annotation
import matplotlib.pyplot as plt
# from adjustText import adjust_text
from os import path

bundle_dir = path.abspath(path.join(path.dirname(__file__), "data"))

window = tk.Tk()
#getting screen width and height of display
width= window.winfo_screenwidth()
height= window.winfo_screenheight()
#setting tkinter window size
window.geometry("%dx%d" % (width, height))
window.config(bg="black")
window.title("AstroGuessr")


fov = tk.StringVar()
ra = tk.StringVar()
dec = tk.StringVar()
ismessier = tk.IntVar()
isconstellation = tk.IntVar()
constellationHint = tk.IntVar()
messierHint = tk.IntVar()
isEquator = tk.IntVar()
isEcliptic = tk.IntVar()
randomRotate = tk.IntVar()
randomFlip = tk.IntVar()

rotation = 0
xFlip = 1
yFlip = 1


print("Loading data")

main_stars = pd.read_csv(path.join(bundle_dir, path.join(bundle_dir, "stars.csv")))
main_constellation = pd.read_csv(path.join(bundle_dir, path.join(bundle_dir, "constellations.csv")))
main_messier = pd.read_csv(path.join(bundle_dir, "messier.csv"))
main_equator = pd.read_csv(path.join(bundle_dir, "equator.csv"))
main_ecliptic = pd.read_csv(path.join(bundle_dir, "ecliptic.csv"))


def hardReset():    
    global rotation
    global xFlip
    global yFlip

    if randomRotate.get():
        rotation = np.random.uniform(0,359) * pi / 180
    else:
        rotation = 0

    if randomFlip.get():
        yFlip = np.random.choice([1,-1])
        xFlip = np.random.choice([1,-1])
    else:
        xFlip = 1
        yFlip = 1
    messierButton.deselect()
    constellationButton.deselect()
    equatorButton.deselect()
    eclipticButton.deselect()
    constellationHintButton.deselect()
    messierHintButton.deselect()
    rotateButton.deselect()
    flipButton.deselect()
    reset()

def reset():
    plt.close()
    global rotation
    global xFlip
    global yFlip
    FOV = fov.get()
    RACENTER = ra.get()
    DECCENTER = dec.get()

    if len(FOV) == 0:
        FOV = np.random.randint(10,90)
        efov.insert(0,str(FOV))
    else:
        FOV = float(FOV)
    if len(RACENTER) == 0:
        RACENTER = np.random.randint(0,360)
        eRa.insert(0,str(RACENTER))
    else:
        RACENTER = float(RACENTER)
    if len(DECCENTER) == 0 :
        DECCENTER = np.random.randint(-90,90)
        eDec.insert(0,str(DECCENTER))
    else:
        DECCENTER = float(DECCENTER)

    FOV = FOV * pi / 180
    DECCENTER = DECCENTER * pi / 180
    RACENTER = RACENTER * pi / 180

    stars = main_stars.copy()
    constellation = main_constellation.copy()
    messier = main_messier.copy()

    #coordinate transform
    stars['newDec'] = pi/2 - np.arccos(np.sin(DECCENTER)*np.sin(stars['Dec']) + np.cos(DECCENTER) * np.cos(stars['Dec']) * np.cos(RACENTER-stars['Ra']))
    stars['newRa'] = np.arctan2(np.cos(stars['Dec']) * np.sin(RACENTER-stars['Ra']) / np.cos(stars['newDec']),
                                (np.sin(stars['Dec']) - np.sin(stars['newDec'])*np.sin(DECCENTER))/(np.cos(DECCENTER)*np.cos(stars['newDec'])))

    constellation['newDec'] = pi/2 - np.arccos(np.sin(DECCENTER)*np.sin(constellation['Dec']) + np.cos(DECCENTER) * np.cos(constellation['Dec']) * np.cos(RACENTER-constellation['Ra']))
    constellation['newRa'] = np.arctan2(np.cos(constellation['Dec']) * np.sin(RACENTER-constellation['Ra']) / np.cos(constellation['newDec']),
                                (np.sin(constellation['Dec']) - np.sin(constellation['newDec'])*np.sin(DECCENTER))/(np.cos(DECCENTER)*np.cos(constellation['newDec'])))

    messier['newDec'] = pi/2 - np.arccos(np.sin(DECCENTER)*np.sin(messier['Dec']) + np.cos(DECCENTER) * np.cos(messier['Dec']) * np.cos(RACENTER-messier['Ra']))
    messier['newRa'] = np.arctan2(np.cos(messier['Dec']) * np.sin(RACENTER-messier['Ra']) / np.cos(messier['newDec']),
                                (np.sin(messier['Dec']) - np.sin(messier['newDec'])*np.sin(DECCENTER))/(np.cos(DECCENTER)*np.cos(messier['newDec'])))

    #checks FOV
    stars = stars[pi/2-stars['newDec'] < FOV]
    constellation = constellation[pi/2-constellation['newDec'] < FOV]
    messier = messier[pi/2-messier['newDec'] < FOV]



    #creates cartesian points
    stars['Size'] = .1+ ((6-stars['Mag']))**3 / 10
    stars['x'] = -1 * np.cos(stars['newRa']+pi/2+rotation) / np.tan((pi/2 + stars['newDec'])/2) * xFlip
    stars['y'] = np.sin(stars['newRa']+pi/2+rotation) / np.tan((pi/2 + stars['newDec'])/2) * yFlip

    if isconstellation.get():
        constellation['x'] = -1 * np.cos(constellation['newRa']+pi/2+rotation) / np.tan((pi/2 + constellation['newDec'])/2) * xFlip
        constellation['y'] = np.sin(constellation['newRa']+pi/2+rotation) / np.tan((pi/2 + constellation['newDec'])/2) * yFlip

    if ismessier.get():
        messier['x'] = -1 * np.cos(messier['newRa']+pi/2+rotation) / np.tan((pi/2 + messier['newDec'])/2) * xFlip
        messier['y'] = np.sin(messier['newRa']+pi/2+rotation) / np.tan((pi/2 + messier['newDec'])/2) * yFlip

    if isEquator.get():
        equator = main_equator.copy()
        equator['newDec'] = pi/2 - np.arccos(np.sin(DECCENTER)*np.sin(equator['Dec']) + np.cos(DECCENTER) * np.cos(equator['Dec']) * np.cos(RACENTER-equator['Ra']))
        equator['newRa'] = np.arctan2(np.cos(equator['Dec']) * np.sin(RACENTER-equator['Ra']) / np.cos(equator['newDec']),
                                (np.sin(equator['Dec']) - np.sin(equator['newDec'])*np.sin(DECCENTER))/(np.cos(DECCENTER)*np.cos(equator['newDec'])))
        equator = equator[pi/2-equator['newDec'] < FOV]
        equator['x'] = -1 * np.cos(equator['newRa']+pi/2+rotation) / np.tan((pi/2 + equator['newDec'])/2) * xFlip
        equator['y'] = np.sin(equator['newRa']+pi/2+rotation) / np.tan((pi/2 + equator['newDec'])/2) * yFlip
        equator.sort_values(['x'],inplace=True)

    if isEcliptic.get():
        ecliptic = main_ecliptic.copy()
        ecliptic['newDec'] = pi/2 - np.arccos(np.sin(DECCENTER)*np.sin(ecliptic['Dec']) + np.cos(DECCENTER) * np.cos(ecliptic['Dec']) * np.cos(RACENTER-ecliptic['Ra']))
        ecliptic['newRa'] = np.arctan2(np.cos(ecliptic['Dec']) * np.sin(RACENTER-ecliptic['Ra']) / np.cos(ecliptic['newDec']),
                                (np.sin(ecliptic['Dec']) - np.sin(ecliptic['newDec'])*np.sin(DECCENTER))/(np.cos(DECCENTER)*np.cos(ecliptic['newDec'])))
        ecliptic = ecliptic[pi/2-ecliptic['newDec'] < FOV]
        ecliptic['x'] = -1 * np.cos(ecliptic['newRa']+pi/2+rotation) / np.tan((pi/2 + ecliptic['newDec'])/2) * xFlip
        ecliptic['y'] = np.sin(ecliptic['newRa']+pi/2+rotation) / np.tan((pi/2 + ecliptic['newDec'])/2) * yFlip
        ecliptic.sort_values(['x'],inplace=True)

    fig,ax = plt.subplots(1,2,figsize=(15, 7.5),facecolor="black")
    
    fig.tight_layout()
    ax[0].axis('off')
    ax[1].axis('off')

    ax[0].scatter(stars["x"].values,stars["y"].values,s=stars['Size'].values,c=stars["Mag"],cmap = "Greys")
    ax[1].scatter(stars["x"].values,stars["y"].values,s=stars['Size'].values,c=stars["Mag"],cmap = "Greys")

    if ismessier.get():
        ax[1].scatter(messier["x"].values,messier["y"].values,s=3,c="red")

    if isEquator.get():
        ax[1].plot(equator['x'].values,equator['y'].values,c="blue")
    if isEcliptic.get():
        ax[1].plot(ecliptic['x'].values,ecliptic['y'].values,c="yellow")

    ax[0].set_facecolor("black")
    ax[1].set_facecolor("black")

    if isconstellation.get():
        for ind in constellation.index:
            ax[1].annotate(constellation['Name'][ind],xy = (constellation['x'][ind],constellation['y'][ind]),xytext = (constellation['x'][ind],constellation['y'][ind]),c="orange")
    if ismessier.get():
        for ind in messier.index:
            ax[1].annotate(messier['Name'][ind],xy = (messier['x'][ind],messier['y'][ind]),xytext = (messier['x'][ind]-.01,messier['y'][ind]-.02),c="red")
    
        # texts = [child for child in ax[1].get_children() if isinstance(child, Annotation)]
        # adjust_text(texts=texts, x=messier['x'], y=messier['y'], avoid_self=False, time_lim=0.1)

    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,column=0,columnspan=8,sticky=tk.N)

def showMessierHint():
    if messierHint.get():
        tMessierHint.delete("1.0","end")
        FOV = float(fov.get()) * pi / 180
        RACENTER = float(ra.get()) * pi / 180
        DECCENTER = float(dec.get()) * pi / 180
        messier = main_messier.copy()
        messier['newDec'] = pi / 2 - np.arccos(np.sin(DECCENTER)*np.sin(messier['Dec']) + np.cos(DECCENTER) * np.cos(messier['Dec']) * np.cos(RACENTER-messier['Ra']))
        messier = messier[pi/2-messier['newDec'] < FOV]
        string = ""
        for ind in messier.index:
            string = string + " " + messier['Name'][ind]
        tMessierHint.insert(tk.END, string)
    else:
        tMessierHint.delete("1.0","end")

    
def showConstellationHint():
    if constellationHint.get():
        tConstellationHint.delete("1.0","end")
        FOV = float(fov.get()) * pi / 180
        RACENTER = float(ra.get()) * pi / 180
        DECCENTER = float(dec.get()) * pi / 180
        constellation = main_constellation.copy()
        constellation['newDec'] = pi / 2 - np.arccos(np.sin(DECCENTER)*np.sin(constellation['Dec']) + np.cos(DECCENTER) * np.cos(constellation['Dec']) * np.cos(RACENTER-constellation['Ra']))
        constellation = constellation[pi/2-constellation['newDec'] < FOV]
        string = ""
        for ind in constellation.index:
            string = string + " " + constellation['Name'][ind]
        tConstellationHint.insert(tk.END, string)
    else:
        tConstellationHint.delete("1.0","end")



lInstructions = tk.Label(window,text = "Enter parameters here, leave blank for random.",bg="black", fg="white")
lfov = tk.Label(window, text = "FOV:",bg="black", fg="white")
lRa = tk.Label(window, text = "RA:",bg="black", fg="white")
lDec = tk.Label(window,text = "DEC:",bg="black", fg="white")
lKey = tk.Label(window,text = "Show Key",bg="black", fg="white")
lHints = tk.Label(window,text = "Show Hints",bg="black", fg="white")

lKey.grid(row = 5,column = 0)
lHints.grid(row = 4,column = 0)
lInstructions.grid(row=0,column=0,columnspan=3)
lfov.grid(row = 1, column = 0, sticky = tk.W, pady = 2)
lRa.grid(row = 1, column = 2, sticky = tk.W, pady = 2)
lDec.grid(row = 1, column = 4, sticky = tk.W, pady = 2)

#hint text boxes
tMessierHint = tk.Text(window,height=1,bg="white",fg="black")
tConstellationHint = tk.Text(window,height=1,bg="white",fg="black")

tMessierHint.grid(row = 4,column=2,columnspan= 2)
tConstellationHint.grid(row = 4,column=5,columnspan= 2)

# entry widgets, used to take entry from user
efov = tk.Entry(window,textvariable=fov,bg="white",fg="black", highlightbackground="#000")
eRa = tk.Entry(window,textvariable=ra,bg="white",fg="black", highlightbackground="#000")
eDec = tk.Entry(window,textvariable=dec,bg="white",fg="black", highlightbackground="#000")

# this will arrange entry widgets
efov.grid(row = 1, column = 1, pady = 2)
eRa.grid(row = 1, column = 3, pady = 2)
eDec.grid(row = 1, column=5,pady=2)

efov.insert("1","45")

messierButton = tk.Checkbutton(window,
                text = "Show Messier Objects",
                variable = ismessier,
                onvalue=1,
                offvalue=0,
                command=reset,bg="black", fg="white"
)
messierHintButton = tk.Checkbutton(window,text = "Messier Hints",variable = messierHint,command = showMessierHint,bg="black", fg="white")
constellationHintButton = tk.Checkbutton(window,text = "Constellation Hints",variable = constellationHint,command = showConstellationHint,bg="black", fg="white")

messierHintButton.grid(row = 4,column = 1,columnspan = 1)
constellationHintButton.grid(row = 4,column = 4,columnspan= 1)

messierButton.grid(row = 5,column = 1)

constellationButton = tk.Checkbutton(window,
                        text = "Show Constellations",
                        variable = isconstellation,
                        command = reset,
                        bg="black", fg="white"
                      
)

constellationButton.grid(row = 5,column = 2)

eclipticButton = tk.Checkbutton(window,text = "Show Ecliptic",variable = isEcliptic,command = reset,bg="black", fg="white")
equatorButton = tk.Checkbutton(window,text = "Show Equator",variable = isEquator,command = reset,bg="black", fg="white")

equatorButton.grid(row = 5,column = 3)
eclipticButton.grid(row = 5,column = 4)

rotateButton = tk.Checkbutton(window,text = "Randomly Rotate",variable = randomRotate,bg="black", fg="white")
flipButton = tk.Checkbutton(window,text = "Randomly Flip",variable = randomFlip,bg="black", fg="white")

rotateButton.grid(row = 0,column = 3)
flipButton.grid(row = 0,column = 4)

resetButton = tk.Button(
                  text = "Reset",
                  command = hardReset, bg="white", fg="black", highlightbackground="#000"
                  )
resetButton.grid(row=1,column=6,pady=2)

print("Ready")

window.mainloop()