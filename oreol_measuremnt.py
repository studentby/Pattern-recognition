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
from skimage.measure import find_contours
from skimage import feature
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

    # Let's find oreol
    edges = feature.canny(filtered_image, sigma=3, low_threshold=0.001, high_threshold=0.01)
    # contours = find_contours(edges, fully_connected='low')

    # for contour in contours:
    #     ax.plot(contour[:, 1], contour[:, 0], linewidth = 2)


    ax.imshow(edges, cmap='gray')
    ax.set_title('Canny filter', fontsize=20)


    fig.tight_layout()
    plt.show()

oreol()