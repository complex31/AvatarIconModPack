import os
from tkinter import *
from PIL import Image
from PIL import ImageTk
import fileinput

overrides = []
paths = []
imageIndices = []
iniFile = open("mod.ini", "r")
for line in iniFile:
    if "TextureOverride" in line:
        overrides.append(line.replace("[TextureOverride", "").replace("]", "").strip())
    if "filename" in line:
        paths.append("/".join(line.split("=")[1].strip().split("\\")[:-1]))
        imageIndices.append(line.split("=")[1].strip().split("\\")[-1].split(".")[0])
iniFile.close()

currentOverride = overrides[0]
currentPath = paths[0]
currentImageIndex = imageIndices[0]

root = Tk() 
root.title("Icon Selector")
root.geometry("600x400")

def previous():
    global currentImageIndex
    available = os.listdir(currentPath)
    currentImageIndex = int(currentImageIndex) - 1
    if (currentImageIndex < 0):
        currentImageIndex = len(available)-1
    currentImageIndex = str(currentImageIndex)
    updateImage()

def next():
    global currentImageIndex
    available = os.listdir(currentPath)
    currentImageIndex = int(currentImageIndex) + 1
    if (currentImageIndex >= len(available)):
        currentImageIndex = 0
    currentImageIndex = str(currentImageIndex)
    updateImage()

def apply():
    print("applying")
    iniFile = open("mod.ini", "r")
    lines = iniFile.readlines()
    iniFile.close()
    i = 0
    while i < (len(lines)):
        if f"[TextureOverride{currentOverride}]" in lines[i]:
            while True:
                if "filename" not in lines[i]:
                    i += 1
                else:
                    parts = lines[i].split("\\")
                    newline = "\\".join(parts[:-1]+[currentImageIndex+"."+parts[-1].split(".")[1]])
                    lines[i] = newline
                    break
        i += 1
    newIniFile = open("mod.ini", "w")
    newIniFile.writelines(lines)
    newIniFile.close


def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    global currentOverride
    currentOverride = overrides[index]
    global currentImageIndex
    currentImageIndex = imageIndices[index]
    global currentPath
    currentPath = paths[index]
    updateImage()

def updateImage():
    global imagecanvas
    global sprite
    global image
    imagePath = f"{currentPath}/{currentImageIndex}.dds"
    pilImage = Image.open(imagePath)
    pilImage = pilImage.transpose(Image.FLIP_TOP_BOTTOM)
    image = ImageTk.PhotoImage(pilImage)
    imagecanvas.itemconfig(sprite, image = image)

editable = fileinput.FileInput("mod.ini", inplace=1)

clicked = StringVar()
clicked.set(overrides[0])

listbox = Listbox(root)
listbox.pack(side = LEFT, fill = Y, padx=(20,0), pady=20) 
scrollbar = Scrollbar(root) 
scrollbar.pack(side = LEFT, fill = Y, padx=(0,20), pady=20)
for value in overrides: 
    listbox.insert(END, value)

listbox.config(yscrollcommand = scrollbar.set)
listbox.bind('<<ListboxSelect>>', onselect)
scrollbar.config(command = listbox.yview)

imagecanvas = Canvas(root,width=256,height=256)
imagecanvas.pack(anchor=CENTER, padx=40, pady=40)
imagePath = f"{currentPath}/{currentImageIndex}.dds"
pilImage = Image.open(imagePath)
pilImage = pilImage.transpose(Image.FLIP_TOP_BOTTOM)
image = ImageTk.PhotoImage(pilImage)
sprite = imagecanvas.create_image(0,0,anchor="nw",image=image)

buttonFrame = Frame(root)
buttonFrame.pack(anchor=CENTER)
previousButton =  Button(root, text = "<<", command = previous)
applyButton =  Button(root, text = "Apply", command = apply)
nextButton =  Button(root, text = ">>", command = next)
previousButton.pack(in_=buttonFrame, anchor=CENTER, side = LEFT, padx=10)
applyButton.pack(in_=buttonFrame, anchor=CENTER, side = LEFT, padx=10)
nextButton.pack(in_=buttonFrame, anchor=CENTER, side = LEFT, padx=10)

root.mainloop() 
