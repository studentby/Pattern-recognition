import matplotlib.pyplot as plt

from tkinter import Image
from PIL import Image
from pyparsing import line_end
from skimage.draw import line

from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.measure import find_contours, approximate_polygon
from skimage.future import graph
from skimage import color, morphology, feature, segmentation, filters, io
import numpy as np

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


labels = segmentation.slic(npImage1, compactness=30, n_segments=1000, start_label=1)
edges = filters.sobel(grayscale_image_1)
edges_rgb = color.gray2rgb(edges)

g = graph.rag_boundary(labels, edges)
lc = graph.show_rag(labels, g, edges_rgb, img_cmap=None, edge_cmap='viridis',
                    edge_width=1.3)

plt.colorbar(lc, fraction=0.03)
io.show()