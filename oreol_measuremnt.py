from cmath import pi
import matplotlib.pyplot as plt
import time
from tkinter import Image
from PIL import Image
from pyparsing import line_end
from skimage.draw import line
import cv2
import math

from skimage.color import rgb2gray
from skimage import morphology, filters
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter
from skimage.measure import find_contours
from skimage import feature, data, color
import numpy as np


def oreol():
    original_image_1 = Image.open("PiSi/PiSi50.jpg")

    # Grayscaling and comparison of original image in MatPlot Lib 
    grayscale_image_1 = rgb2gray(original_image_1)

    # Showing made changes on Plot and comparing with Original 
    fig, ax = plt.subplots(figsize=(8, 4))


    # Removal of small objects from Image
    footprint_1 = morphology.disk(15)
    res_1 = morphology.white_tophat(grayscale_image_1, footprint_1)
    filtered_image = grayscale_image_1 - res_1
    gaussian_filter = cv2.GaussianBlur(filtered_image, (17,19), cv2.BORDER_DEFAULT)

    # Let's find oreol
    edges = feature.canny(gaussian_filter, sigma=3, low_threshold=0.01, high_threshold=0.02)
    
    hough_radii = np.arange(400, 1000, 100)
    hough_res = hough_circle(edges, hough_radii)

    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=7, min_xdistance=50, min_ydistance=50)
    image = color.gray2rgb(gaussian_filter)

    radii_list = []
    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius,
                                        shape=image.shape)
        image[circy, circx] = (250, 0, 0) # Circle color (R, G, B)
        radii_list.append(radius)
    ax.imshow(image, cmap=plt.cm.gray)
    ax.set_title('Oreol measurement', fontsize=20)

    # Finding average radii from list
    avg_radius = np.median(radii_list)
    print(avg_radius)

    # Scale 6mkm around 833 pixels for PiSi50
    scale = 833

    # Scale length in mkm
    scale_length = 6


    avg_radius = avg_radius/scale*scale_length
    # Oreol area in pixels
    oreoll_area = pi * avg_radius * avg_radius
    print(oreoll_area)

    fig.tight_layout()
    plt.show()

oreol()