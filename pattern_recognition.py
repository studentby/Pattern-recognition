from html import parser
import matplotlib.pyplot as plt
from cmath import pi
import time
from tkinter import Image
from PIL import Image
from pyparsing import line_end
from skimage.draw import circle_perimeter
# import cv2
import math
import argparse

from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.measure import find_contours, approximate_polygon, perimeter
from skimage.future import graph
from skimage import color, morphology, feature, segmentation, filters, io
from skimage.transform import hough_circle, hough_circle_peaks
import numpy as np

parser = argparse.ArgumentParser()

path = parser.add_argument("--path", "--p", help="path to image", default="PiSi/PiSi50.jpg")
scale = parser.add_argument("--scale", "--sc", help="lenght of a single scale in pixels", default=833)
length = parser.add_argument("--length", "--l", help="length of a single scale in mkm", default=5)

args = parser.parse_args()
def main():

    original_image_1 = Image.open(args.path)

    # Grayscaling and comparison of original image in MatPlot Lib 
    grayscale_image_1 = rgb2gray(original_image_1)

    # Showing made changes on Plot and comparing with Original 
    fig, ax = plt.subplots(figsize=(8, 4))

    # Removal of small objects from Image
    footprint_1 = morphology.disk(3)
    res_1 = morphology.white_tophat(grayscale_image_1, footprint_1)
    filtered_image = grayscale_image_1 - res_1
    gaussian_filter = cv2.GaussianBlur(filtered_image, (17,19), 0)

    edges = feature.canny(gaussian_filter, sigma=3, low_threshold=0.01, high_threshold=0.02)
    # Image rendition
    # ax.imshow(gaussian_filter, cmap=plt.cm.gray)

    ax.set_xticks([]), ax.set_yticks([])
    ax.set_title("Pattern Recognition", fontsize = 20)

    contours_1 = find_contours(gaussian_filter, fully_connected='high', positive_orientation='high')
    area_list = []

    # Scale length in mk metters 
    scale_length = math.pow(int(args.length), -6)

    for contour in contours_1:
        coords = approximate_polygon(contour, tolerance = 50)
        ax.plot(coords[:, 1], coords[:, 0], '-r', linewidth = 2)
        ax.plot(contour[:, 1], contour[:, 0], linewidth = 1)
        if len(coords) == 5:
            
            # Dioganals of squares
            diogan_1 = math.sqrt(math.pow(coords[0][0]-coords[2][0],2) + math.pow(coords[0][1]-coords[2][1], 2))
            diogan_2 = math.sqrt(math.pow(coords[1][0]-coords[3][0],2) + math.pow(coords[1][1]-coords[3][1], 2))
            

            # Rounding with two decimals
            scaled_diogan_1 = scale_length * diogan_1/args.scale
            scaled_diogan_2 = scale_length * diogan_2/args.scale

            # Area by diogonals and diveded by two

            area = scaled_diogan_1*scaled_diogan_1/2

            print("First dioganal: " + str(scaled_diogan_1))
            print("Second dioganal: " + str(scaled_diogan_2))
            print("Found Area of polygone: " + str(area))

            # P - gramm pressure (нагрузка)
            P = 50 * math.pow(10,-3)

            H = 1.854 * P / (scaled_diogan_1 * scaled_diogan_2)
            print("H: " + str(round(H,3)))
            
            area_list.append(area)            
            # Measuring area by cv2 with Grins algorithm
            # c = np.expand_dims(contour.astype(np.float32), 1)
            # # Convert it to UMat object
            # c = cv2.UMat(c)
            # area_c = cv2.contourArea(c)
            # print("OpenCV measured area: ", area_c)
    
    if len(area_list) != 0:
        area_diff = str((abs(area_list[0]-area_list[1]),2))
        print(area_diff + " mkm2 - Area Differnce")
    
    ## Let's find oreol 
    
    hough_radii = np.arange(300, 900, 100)
    hough_res = hough_circle(edges, hough_radii)

    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=2, min_xdistance=100, min_ydistance=100)
    image = color.gray2rgb(gaussian_filter)

    radii_list = []
    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius,
                                        shape=image.shape)
        image[circy, circx] = (0, 0, 250) # Circle color (R, G, B)
        # print("Found Radius oreol: " + str(radius) + " pixels")
        radii_list.append(radius)
    ax.imshow(image, cmap=plt.cm.gray)

    # Finding average radii from list
    median_radius = np.median(radii_list)
    print("Median radius: " + str(median_radius))

    median_radius_scaled = median_radius/args.scale*scale_length
    # Oreol area in pixels
    oreoll_area = pi * median_radius_scaled * median_radius_scaled
    print("Oreol area: " + str(oreoll_area))

    fig.tight_layout()
    
if __name__=="__main__":
    start_time = time.time()
    main()
    print("--- Execution %s seconds ---" % round(time.time() - start_time))
    plt.show()