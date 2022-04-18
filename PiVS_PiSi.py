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
    original_image = Image.open("Pi/Pi50.jpg")
    original_image_1 = Image.open("PiSi/PiSi50.jpg")

    im_array = np.array(original_image)
    im1_array = np.array(original_image_1)

    # Image saved in numPy array
    npImage = Image.fromarray(im_array, 'RGB')
    npImage1 = Image.fromarray(im1_array, 'RGB')

    # Grayscaling and comparison of original image in MatPlot Lib 
    grayscale_image = rgb2gray(original_image)
    grayscale_image_1 = rgb2gray(original_image_1)

    # Showing made changes on Plot and comparing with Original 
    fig, ax = plt.subplots(figsize=(8, 4))

    # Removal of small objects from Image
    footprint_1 = morphology.disk(5)
    res_1 = morphology.white_tophat(grayscale_image_1, footprint_1)

    # Detecting Edges 
    edges1 = feature.canny(grayscale_image_1 - res_1, sigma = 2)

    # Image rendition
    ax.imshow(grayscale_image_1 - res_1, cmap=plt.cm.gray)

    ax.set_xticks([]), ax.set_yticks([])
    ax.set_title("PiSi", fontsize = 20)

    contours_1 = find_contours(grayscale_image_1 - res_1, fully_connected='high')

    area_list = []

    for contour in contours_1:
        coords = approximate_polygon(contour, tolerance = 60)
        ax.plot(coords[:, 1], coords[:, 0], '-r', linewidth = 1)
        ax.plot(contour[:, 1], contour[:, 0], linewidth = 2)
        if len(coords) == 5:
            print(coords)
            # coords[x][y]

            #Dioganals of squares
            diogan_1 = math.sqrt(math.pow(coords[0][0]-coords[2][0],2) + math.pow(coords[0][1]-coords[2][1], 2))
            diogan_2 = math.sqrt(math.pow(coords[1][0]-coords[3][0],2) + math.pow(coords[1][1]-coords[3][1], 2))
            
            # Scale 6mm around 833 pixels
            scale = 833

            # Scale length in mm
            scale_length = 6

            # Rounding with two decimals
            scaled_diogan_1 = diogan_1/scale*scale_length
            scaled_diogan_2 = diogan_2/scale*scale_length

            # Area by diogonals and diveded by two
            area = scaled_diogan_1*scaled_diogan_1/2
            print("First dioganal: " + str(round(scaled_diogan_1, 2)))
            print("Second dioganal: " + str(round(scaled_diogan_2, 2)))
            
            # Contour area
            # c = np.expand_dims(coords.astype(np.float32), 1)
            # # Convert it to UMat object 
            # c = cv2.UMat(c)
            # area = cv2.contourArea(c)
            # print("Area of contour: " + str(area))
            area_list.append(area)
    print(area_list)
    area_diff = str(abs(area_list[0]-area_list[1]))
    print(area_diff + "mm2 - Area Differnce" )
        
    fig.tight_layout()

if __name__=="__main__":
    start_time = time.time()
    main()
    print("---Execution %s seconds ---" % round(time.time() - start_time))
    plt.show()
    
# npImage.save('/home/ububntu/Desktop/Diploma/squrePatterns/image_test.png')