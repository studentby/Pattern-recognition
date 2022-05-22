import matplotlib.pyplot as plt
from cmath import pi
import time
from PIL import Image
from skimage.draw import circle_perimeter
import math

from skimage.color import rgb2gray
from skimage.measure import find_contours, approximate_polygon
from skimage import color, morphology
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.filters import gaussian
import numpy as np

def userInput():

    userInput.path = input("Enter image full path: ")
    userInput.scale = int(input ("Scale number in pixels: "))
    userInput.length = int(input("Length of a single scale: "))
    # userInput.path = "PiSi/PiSi50.jpg"
    # userInput.scale = int(833)
    # userInput.length = int(5)

def main():

    userInput()

    original_image_1 = Image.open(userInput.path)

    # Grayscaling and comparison of original image in MatPlot Lib 
    grayscale_image_1 = rgb2gray(original_image_1)

    # Showing made changes on Plot and comparing with Original 
    fig, main.ax = plt.subplots(figsize=(8, 4))

    # Removal of small objects from Image
    footprint_1 = morphology.disk(3)
    res_1 = morphology.white_tophat(grayscale_image_1, footprint_1)
    filtered_image = grayscale_image_1 - res_1
    main.gaussian_filter = gaussian(filtered_image, 3, preserve_range=False)

    # main.edges = canny(main.gaussian_filter, sigma=3, low_threshold=0.01, high_threshold=0.02)

    main.ax.set_xticks([]), main.ax.set_yticks([])
    main.ax.set_title("Pattern Recognition", fontsize = 20)

    contours_1 = find_contours(main.gaussian_filter, fully_connected='high', positive_orientation='high')
    area_list = []

    # Scale length in mk metters 
    main.scale_length = math.pow(int(userInput.length), -6)

    for contour in contours_1:
        coords = approximate_polygon(contour, tolerance = 50)
        main.ax.plot(coords[:, 1], coords[:, 0], '-r', linewidth = 2)
        main.ax.plot(contour[:, 1], contour[:, 0], linewidth = 1)
        if len(coords) == 5:
            
            # Dioganals of squares
            diogan_1 = math.sqrt(math.pow(coords[0][0]-coords[2][0],2) + math.pow(coords[0][1]-coords[2][1], 2))
            diogan_2 = math.sqrt(math.pow(coords[1][0]-coords[3][0],2) + math.pow(coords[1][1]-coords[3][1], 2))
            

            # Rounding with two decimals
            scaled_diogan_1 = main.scale_length * diogan_1/userInput.scale
            scaled_diogan_2 = main.scale_length * diogan_2/userInput.scale

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
    
    main.ax.imshow(main.gaussian_filter, cmap=plt.cm.gray)
    fig.tight_layout()
    
    ## Let's find oreol 
def oreol():
    hough_radii = np.arange(300, 900, 100)
    hough_res = hough_circle(main.edges, hough_radii)

    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=2, min_xdistance=100, min_ydistance=100)
    image = color.gray2rgb(main.gaussian_filter)

    radii_list = []
    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius,
                                        shape=image.shape)
        image[circy, circx] = (0, 0, 250) # Circle color (R, G, B)
        radii_list.append(radius)
    main.ax.imshow(main.gaussian_filter, cmap=plt.cm.gray)

    # Finding average radii from list
    median_radius = np.median(radii_list)
    print("Median radius: " + str(median_radius))

    median_radius_scaled = median_radius/userInput.scale * main.scale_length
    # Oreol area in pixels
    oreoll_area = pi * median_radius_scaled * median_radius_scaled
    print("Oreol area: " + str(oreoll_area))

   
    
if __name__=="__main__":
    start_time = time.time()
    main()
    print("--- Execution %s seconds ---" % round(time.time() - start_time))
    plt.show()