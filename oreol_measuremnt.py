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
from pattern_recognition import main

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