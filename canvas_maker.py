import PySimpleGUI as sg
import os.path
from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
import glob
import itertools
import timeit
import shutil
import os
pathim = "temp/"
# Check whether the specified path exists or not
isExist = os.path.exists(pathim)
if not isExist:
    os.makedirs(pathim)
    print("The new directory is created!")



def func(message):
    print(message)

layout1 = [[
            sg.In("Choose the Room",size=(40, 2), enable_events=True, key="-ROOMI-"), 
            sg.FileBrowse("Choose the Room",size=(20, 1), key="-ROOM-")
          ],
    
           [
            sg.In("Choose the Painting",size=(40, 2), enable_events=True, key="-PAINTINGI-"),
            sg.FileBrowse("Choose the Painting",size=(20, 1),  key="-PAINTING-")
           ],
    
            [
            sg.Button("MAKE CANVAS", key = "-EDIT-",size=(57, 1))
          ]] 
        
window = sg.Window('Canvas Maker', layout= layout1, margins=(100, 50))

while True:             # Event Loop

    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    try:
        if event == '-ROOMI-':
            room = values['-ROOM-'].split("/")[-1]
            print(values['-ROOM-'].split("/")[-1])
            sg.Popup("Room has been saved")
                
        elif event == '-PAINTINGI-':
            painting = values['-PAINTING-'].split("/")[-1]
            print(values['-PAINTING-'].split("/")[-1])
            sg.Popup("Painting has been saved")
        elif event == '-EDIT-':
            window.Close()
        
    except:
        func("Something went wrong and i am too lazy to figure out")
        
        



import cv2
import numpy as np
from PIL import Image

dosya = room
img = cv2.imread(dosya)
height, width, channels = img.shape

dosya2 = painting
img2 = cv2.imread(dosya2)
h2, w2, channels = img2.shape

inputs =  np.float32([[0,0], [w2,0], [w2,h2], [0, h2]])


def resize_by_percentage(image, outfile, percentage):
    with Image.open (image) as im:
        width, height = im.size
        resized_dimensions = (int(width * percentage), int(height * percentage))
        resized = im.resize(resized_dimensions)
        resized.save(outfile)


def paste():
    background = Image.open(dosya)
    foreground = Image.open("temp/transparent.png")

    background.paste(foreground, (0, 0), foreground)
    background.show()
    background.save("temp/pasted.png", "PNG")
    
def convertImage():
    img = Image.open("temp/warped.png")
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
 
    img.putdata(newData)
    img.save("temp/transparent.png", "PNG")
    print("Successful")
    
    
def pastam(x, y):
    background = Image.open(room).convert('RGBA')
    foreground = Image.open("temp/normalized.png").convert('RGBA')

    background.paste(foreground, (x, y), foreground)
    background.show()
    background.save("final.png")




def click_event(event, x, y, flags, params):
    
    img = cv2.imread(dosya)
    height, width, channels = img.shape

    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        kd.append([x, y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        if len(kd)%2== 0:
            w = kd[-1][0] - kd[-2][0]
            h = kd[-1][1] - kd[-2][1]
            img_cropped = img[kd[-2][1]:kd[-2][1]+h, kd[-2][0]:kd[-2][0]+w]
            #img = img[57:57+110, 229:229+57]
            cv2.imwrite(f"temp/cropped_{dosya}", img_cropped)
            
            
            resize_by_percentage(f"temp/cropped_{dosya}","temp/4kat.png", 4)
            zoomed = cv2.imread("temp/4kat.png")
            cv2.destroyAllWindows()
            
        cv2.putText(img, str(x) + ',' + str(y), (x,y), font, 1, (255, 0, 0), 2)
        cv2.imshow('image', img)
        
        
def click_eventiki(eventiki, x, y, flags, params):

    if eventiki == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        kp.append([x, y])
        if len(kp)%4 == 0:
            fark = kp[-3][1] - kp[-4][1]
            #outputs = np.float32([kp[-4], kp[-3], [kp[-3][0], kp[-2][1]], [kp[-4][0], kp[-1][1]]])   # starting from upper left corner, clockwise
            outputs = np.float32([kp[-4], kp[-3], kp[-2], kp[-1]]) 
            matrix = cv2.getPerspectiveTransform(inputs,outputs)
            imgOutput = cv2.warpPerspective(img2, matrix, (width,height), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
            cv2.imwrite("temp/warped.png", imgOutput)
            convertImage()
            paste()
            resize_by_percentage(f"temp/pasted.png","temp/normalized.png", 0.25)
            pastam(kd[0][0], kd[0][1])
            cv2.destroyAllWindows()
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        

if __name__=="__main__":
    kd = []
    img = cv2.imread(dosya, 1)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if os.path.exists("temp/4kat.png"):
        dosya = "temp/4kat.png"
        img = cv2.imread(dosya)
        h, w, channels = img.shape
        width = w
        height = h
        kp = []
        imge = cv2.imread("temp/4kat.png", 1)
        cv2.imshow('Imagine', imge)
        cv2.setMouseCallback('Imagine', click_eventiki)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if os.path.exists("final.png"):
            cv2.destroyAllWindows()
        
        folder = 'temp/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    
