import matplotlib.pyplot as plt
from cmath import pi
import time
from PIL import Image
from skimage.draw import circle_perimeter
import cv2
import math

from skimage.color import rgb2gray
from skimage.measure import find_contours, approximate_polygon
from skimage import color, morphology
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks
import numpy as np

def userInput():

    # userInput.path = input("Enter image full path: ")
    # userInput.scale = int(input ("Scale number in pixels: "))
    # userInput.length = int(input("Length of a single scale: "))
    userInput.path = "C:/Users/Ayhan_Gylychmammedov/Desktop/Learn/little_projects/Pattern-recognition/PiSi/PiSi50.jpg"
    userInput.scale = int(833)
    userInput.length = int(5)

def main():

    userInput()

    original_image_1 = Image.open(userInput.path)

    # Grayscaling and comparison of original image in MatPlot Lib 
    grayscale_image_1 = rgb2gray(original_image_1)

    # Showing made changes on Plot and comparing with Original 
    fig, ax = plt.subplots(figsize=(8, 4))

    # Removal of small objects from Image
    footprint_1 = morphology.disk(3)
    res_1 = morphology.white_tophat(grayscale_image_1, footprint_1)
    filtered_image = grayscale_image_1 - res_1
    gaussian_filter = cv2.GaussianBlur(filtered_image, (17,19), 0)

    edges = canny(gaussian_filter, sigma=3, low_threshold=0.01, high_threshold=0.02)

    ax.set_xticks([]), ax.set_yticks([])
    ax.set_title("Pattern Recognition", fontsize = 20)

    contours_1 = find_contours(gaussian_filter, fully_connected='high', positive_orientation='high')
    area_list = []

    # Scale length in mk metters 
    scale_length = math.pow(int(userInput.length), -6)

    for contour in contours_1:
        coords = approximate_polygon(contour, tolerance = 50)
        ax.plot(coords[:, 1], coords[:, 0], '-r', linewidth = 2)
        ax.plot(contour[:, 1], contour[:, 0], linewidth = 1)
        if len(coords) == 5:
            
            # Dioganals of squares
            diogan_1 = math.sqrt(math.pow(coords[0][0]-coords[2][0],2) + math.pow(coords[0][1]-coords[2][1], 2))
            diogan_2 = math.sqrt(math.pow(coords[1][0]-coords[3][0],2) + math.pow(coords[1][1]-coords[3][1], 2))
            

            # Rounding with two decimals
            scaled_diogan_1 = scale_length * diogan_1/userInput.scale
            scaled_diogan_2 = scale_length * diogan_2/userInput.scale

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
        radii_list.append(radius)
    ax.imshow(image, cmap=plt.cm.gray)

    # Finding average radii from list
    median_radius = np.median(radii_list)
    print("Median radius: " + str(median_radius))

    median_radius_scaled = median_radius/userInput.scale*scale_length
    # Oreol area in pixels
    oreoll_area = pi * median_radius_scaled * median_radius_scaled
    print("Oreol area: " + str(oreoll_area))

    fig.tight_layout()
    
if __name__=="__main__":
    start_time = time.time()
    main()
    print("--- Execution %s seconds ---" % round(time.time() - start_time))
    plt.show()