import matplotlib.pyplot as plt

from tkinter import Image
from PIL import Image
from pyparsing import line_end
from skimage.draw import line

from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.measure import find_contours, approximate_polygon
from skimage import color, morphology
import numpy as np

# Local paths to images
original_image = Image.open("/home/ububntu/Desktop/Diploma/PoSi/41_50gramm.jpg")
original_image_1 = Image.open("/home/ububntu/Desktop/Diploma/PoSi/PoSi.jpg")

# im.convert('L')

im_array = np.array(original_image)
im1_array = np.array(original_image_1)

# Image saved in numPy array
npImage = Image.fromarray(im_array, 'RGB')
npImage1 = Image.fromarray(im1_array, 'RGB')

# Grayscaling and comparison of original image in MatPlot Lib 
grayscale_image = rgb2gray(original_image)
grayscale_image_1 = rgb2gray(original_image_1)

# s = np.linspace(0, 2 * np.pi, 400)
# r =  568 + 200*np.cos(s) # x -coordinate
# c = 841 + 200*np.sin(s) # y - coordinate
# init = np.array([r, c]).T



# snake = active_contour(gaussian(grayscale_image, 3, preserve_range=False),
#                        init, alpha=0.015, beta=10, gamma=0.001)


# Showing made changes on Plot and comparing with Original 
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
ax = axes.ravel()

# Show conturus on picture
footprint = morphology.disk(2)
res = morphology.white_tophat(grayscale_image,footprint)

contours = find_contours(grayscale_image - res, fully_connected='low')
for contour in contours:
    ax[1].plot(contour[:, 1], contour[:, 0], linewidth = 1)  


footprint_1 = morphology.disk(2)
res_1 = morphology.white_tophat(grayscale_image_1,footprint_1)


ax[1].imshow(grayscale_image - res, cmap=plt.cm.gray)
ax[0].imshow(grayscale_image_1 - res_1, cmap=plt.cm.gray)
# ax[1].plot(init[:, 1], init[:, 0], '--r', lw=3)
# ax[1].plot(snake[:, 1], snake[:, 0], '-b', lw=3)


ax[0].set_xticks([]), ax[0].set_yticks([])
ax[1].set_xticks([]), ax[1].set_yticks([])

ax[1].axis([0, grayscale_image.shape[1], grayscale_image.shape[0], 0])

ax[1].set_title("№41 50 gramm pressure")
ax[0].set_title("PolySi")

# Drawing square
coordinates = np.array(
    [line(1677, 1279, 1850, 1125),
    line(1850, 1125, 2025, 1280),
    line(2025, 1280, 1850, 1460),
    line(1850, 1460, 1677, 1279)],
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
    ax[0].plot(line_draw_1[:, 0],line_draw_1[:, 1],'--w',lw=1)

contours_1 = find_contours(grayscale_image_1 - res_1, fully_connected='low')
for contour in contours_1:
    ax[0].plot(contour[:, 1], contour[:, 0], linewidth = 3) 

fig.tight_layout()
plt.show()

# npImage.save('/home/ububntu/Desktop/Diploma/squrePatterns/image_test.png')