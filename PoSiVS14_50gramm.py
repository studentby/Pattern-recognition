from email.mime import image
import matplotlib.pyplot as plt
import time
from tkinter import Image
from PIL import Image
from pyparsing import line_end
from skimage.draw import line
import cv2
import math

from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.measure import find_contours, approximate_polygon, perimeter
from skimage.future import graph
from skimage import color, morphology, feature, segmentation, filters, io
import numpy as np


def main():

    original_image = Image.open("PoSi/14_50gramm.jpg")
    original_image_1 = Image.open("PoSi/PoSi.jpg")

    # im.convert('L')

    im_array = np.array(original_image)
    im1_array = np.array(original_image_1)

    # Image saved in numPy array
    npImage = Image.fromarray(im_array, 'RGB')
    npImage1 = Image.fromarray(im1_array, 'RGB')

    # Grayscaling and comparison of original image in MatPlot Lib 
    grayscale_image = rgb2gray(original_image)
    grayscale_image_1 = rgb2gray(original_image_1)

    # Showing made changes on Plot and comparing with Original 
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    ax = axes.ravel()

    # Show conturus on picture
    footprint = morphology.disk(10)
    res = morphology.white_tophat(grayscale_image,footprint)

    contours = find_contours(grayscale_image - res, fully_connected='high')
    for contour in contours:
        ax[1].plot(contour[:, 1], contour[:, 0], linewidth = 1)  

    footprint_1 = morphology.disk(5)
    res_1 = morphology.white_tophat(grayscale_image_1, footprint_1)

    # Image rendition
    ax[1].imshow(original_image_1, cmap=plt.cm.gray)
    ax[0].imshow(grayscale_image_1 - res_1, cmap=plt.cm.gray)


    ax[0].set_xticks([]), ax[0].set_yticks([])
    ax[1].set_xticks([]), ax[1].set_yticks([])

    ax[1].axis([0, grayscale_image.shape[1], grayscale_image.shape[0], 0])

    ax[1].set_title("№14 50 gramm pressure", fontsize = 20)
    ax[0].set_title("PolySi", fontsize = 20)

    contours_1 = find_contours(grayscale_image_1 - res_1, fully_connected='high')

    for contour in contours_1:
        coords = approximate_polygon(contour, tolerance = 60)
        # ax[0].plot(coords[:, 1], coords[:, 0], '-r', linewidth = 1)
        # ax[0].plot(contour[:, 1], contour[:, 0], linewidth = 2)
        if len(coords) == 4:
            print(coords)
            # coords[x][y]
            print(math.sqrt(math.pow(coords[0][0]-coords[2][0],2) + math.pow(coords[0][1]-coords[2][1], 2)))
            print(math.sqrt(math.pow(coords[1][0]-coords[3][0],2) + math.pow(coords[1][1]-coords[3][1], 2)))
            
            c = np.expand_dims(coords.astype(np.float32), 1)
            # Convert it to UMat object
            c = cv2.UMat(c)
            area = cv2.contourArea(c)
            # print(area)
        
        
    fig.tight_layout()

if __name__=="__main__":
    start_time = time.time()
    main()
    print("---Execution %s seconds ---" % round(time.time() - start_time))
    plt.show()
    
# npImage.save('/home/ububntu/Desktop/Diploma/squrePatterns/image_test.png')