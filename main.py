import cv2
import numpy as np
from PIL import Image

dosya = "76.png"

img = cv2.imread(dosya)


width = 512
height = 640

outputs = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])


def click_event(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        kd.append([x, y])
        if len(kd)%4 == 0:
            inputs = np.float32([kd[-4], kd[-3], kd[-2], kd[-1]])   # starting from upper left corner, clockwise
            matrix = cv2.getPerspectiveTransform(inputs,outputs)
            imgOutput = cv2.warpPerspective(img, matrix, (width,height), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
            cv2.imwrite("warped.png", imgOutput)
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(img, str(x) + ',' + str(y), (x,y), font, 1, (255, 0, 0), 2)
        #cv2.imshow('image', img)

if __name__=="__main__":
    kd = []
    img = cv2.imread(dosya, 1)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    image = "warped.png"
    dest = "warped_transparent.png"

    img = Image.open(image)
    img.putalpha(127)  # Half alpha; alpha argument must be an int
    img.save(dest)
