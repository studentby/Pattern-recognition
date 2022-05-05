import matplotlib.pyplot as plt
from cmath import pi
import time
from tkinter import Image
from PIL import Image
from pyparsing import line_end
from skimage.draw import circle_perimeter
import cv2
import math

from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.measure import find_contours, approximate_polygon, perimeter
from skimage.future import graph
from skimage import color, morphology, feature, segmentation, filters, io
from skimage.transform import hough_circle, hough_circle_peaks
import numpy as np


def main():

    original_image_1 = Image.open("PiSi/PiSi50.jpg")

    # Grayscaling and comparison of original image in MatPlot Lib 
    grayscale_image_1 = rgb2gray(original_image_1)

    # Showing made changes on Plot and comparing with Original 
    fig, ax = plt.subplots(figsize=(8, 4))

    # Removal of small objects from Image
    footprint_1 = morphology.disk(5)
    res_1 = morphology.white_tophat(grayscale_image_1, footprint_1)
    filtered_image = grayscale_image_1 - res_1
    gaussian_filter = cv2.GaussianBlur(filtered_image, (17,19), 0)

    # Image rendition
    ax.imshow(gaussian_filter, cmap=plt.cm.gray)

    ax.set_xticks([]), ax.set_yticks([])
    ax.set_title("Polyimide Silicium 50 gramm pressure", fontsize = 20)

    contours_1 = find_contours(gaussian_filter, fully_connected='high')
    area_list = []

    for contour in contours_1:
        coords = approximate_polygon(contour, tolerance = 60)
        ax.plot(coords[:, 1], coords[:, 0], '-r', linewidth = 1)
        ax.plot(contour[:, 1], contour[:, 0], linewidth = 2)
        if len(coords) == 5:
            
            # Dioganals of squares
            diogan_1 = math.sqrt(math.pow(coords[0][0]-coords[2][0],2) + math.pow(coords[0][1]-coords[2][1], 2))
            diogan_2 = math.sqrt(math.pow(coords[1][0]-coords[3][0],2) + math.pow(coords[1][1]-coords[3][1], 2))
            
            # Scale 6mkm around 833 pixels
            scale = 833

            # Scale length in mkm
            scale_length = 20

            # Rounding with two decimals
            scaled_diogan_1 = diogan_1/scale*scale_length
            scaled_diogan_2 = diogan_2/scale*scale_length

            # Area by diogonals and diveded by two

            area = scaled_diogan_1*scaled_diogan_1/2
            
            print("First dioganal: " + str(round(scaled_diogan_1, 2)))
            print("Second dioganal: " + str(round(scaled_diogan_2, 2)))
            print(area)

            # P - gramm pressure
            P = 50

            H = 1.854 * P / (scaled_diogan_1 * scaled_diogan_2)
            print("H: " + str(round(H,3)))
            
            area_list.append(area)
            
            # Measuring area by cv2 with Grins algorithm
            c = np.expand_dims(contour.astype(np.float32), 1)
            # Convert it to UMat object
            c = cv2.UMat(c)
            area_c = cv2.contourArea(c)
            print("OpenCV measured area: ", area_c)
    
    
    area_diff = str(round(abs(area_list[0]-area_list[1]),2))
    print(area_diff + " mkm2 - Area Differnce")
    
    ## Let's find oreol 
    edges = feature.canny(gaussian_filter, sigma=3, low_threshold=0.01, high_threshold=0.02)
    
    hough_radii = np.arange(400, 800, 50)
    hough_res = hough_circle(edges, hough_radii)

    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=2, min_xdistance=150, min_ydistance=150)
    image = color.gray2rgb(gaussian_filter)

    radii_list = []
    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius,
                                        shape=image.shape)
        image[circy, circx] = (250, 0, 0) # Circle color (R, G, B)
        print("Found Radius oreol: " + str(radius) + " pixels")
        radii_list.append(radius)
    ax.imshow(image, cmap=plt.cm.gray)

    # Finding average radii from list
    avg_radius = np.median(radii_list)
    print(avg_radius)

    avg_radius = avg_radius/scale*scale_length
    # Oreol area in pixels
    oreoll_area = pi * avg_radius * avg_radius
    print(oreoll_area)




    fig.tight_layout()
    
if __name__=="__main__":
    start_time = time.time()
    main()
    print("---Execution %s seconds ---" % round(time.time() - start_time))
    plt.show()