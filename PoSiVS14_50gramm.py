from email.mime import image
import matplotlib.pyplot as plt
import time
from tkinter import Image
from PIL import Image
from pyparsing import line_end
from skimage.draw import line
import cv2

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

    footprint_1 = morphology.disk(10)
    res_1 = morphology.white_tophat(grayscale_image_1, footprint_1)

    # Detecting Edges 
    # edges = feature.canny(grayscale_image, sigma = 5)
    # edges1 = feature.canny(grayscale_image_1,sigma = 5)

    # Image rendition
    ax[1].imshow(grayscale_image, cmap=plt.cm.gray)
    ax[0].imshow(grayscale_image_1, cmap=plt.cm.gray)


    ax[0].set_xticks([]), ax[0].set_yticks([])
    ax[1].set_xticks([]), ax[1].set_yticks([])

    ax[1].axis([0, grayscale_image.shape[1], grayscale_image.shape[0], 0])

    ax[1].set_title("№14 50 gramm pressure", fontsize = 20)
    ax[0].set_title("PolySi", fontsize = 20)

    # Drawing square with coordinates (x1,y1,x2,y2)

    coordinates = np.array(
        [line(2208, 1688, 2085, 1564),
        line(2085, 1564, 2207, 1453),
        line(2207, 1453, 2336, 1564),
        line(2336, 1564, 2208, 1688)],
        dtype=list)

    for i in range(len(coordinates)):
        rr, cc = coordinates[i]
        line_draw = np.array([rr,cc]).T 
        ax[1].plot(line_draw[:, 0],line_draw[:, 1],'--b',lw=1)

    coordinates_1 = np.array(
        [line(1769, 1191, 1727, 1154),
        line(1727, 1154, 1769, 1116),
        line(1769, 1116, 1812, 1154),
        line(1812, 1154, 1769, 1191)],
        dtype=list)



    for i in range(len(coordinates_1)):
        rr_1, cc_1 = coordinates_1[i]
        line_draw_1 = np.array([rr_1,cc_1]).T 
        ax[0].plot(line_draw_1[:, 0],line_draw_1[:, 1],'--w', lw = 1)

    contours_1 = find_contours(grayscale_image_1 - res_1, fully_connected='high')
    
    for contour in contours_1:
        coords = approximate_polygon(contour, tolerance = 40)
        ax[0].plot(coords[:, 1], coords[:, 0], '-r', linewidth = 1)
        ax[0].plot(contour[:, 1], contour[:, 0], linewidth = 2)
        if len(coords) == 4:
            print(len(coords))
            print(coords)
            c = np.expand_dims(coords.astype(np.float32), 1)
            # Convert it to UMat object
            c = cv2.UMat(c)
            area = cv2.contourArea(c)
            print(area)
        
        
    fig.tight_layout()

if __name__=="__main__":
    start_time = time.time()
    main()
    print("---Execution %s seconds ---" % round(time.time() - start_time))
    # plt.show()
    
# npImage.save('/home/ububntu/Desktop/Diploma/squrePatterns/image_test.png')