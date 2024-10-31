import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = mpimg.imread("Lenna.png") 

img_resized = np.array(img)
img_resized = img_resized[::int(img.shape[0]/128),::int(img.shape[1]/128)]

plt.imshow(img_resized)
plt.show()