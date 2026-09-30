import cv2  
import numpy as np
from skimage import feature, color, io
import matplotlib.pyplot as plt

def LoG(): 
    image = color.rgb2gray(io.imread("polka_dots_3.jpg"))
    blobs_log = feature.blob_log(image, max_sigma=30, num_sigma=10, threshold=0.1)
    
    # Compute radii
    blobs_log[:, 2] = blobs_log[:, 2] * (2 ** 0.5)
    
    # Display
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray')
    for y, x, r in blobs_log:
        c = plt.Circle((x, y), r, color='red', linewidth=2, fill=False)
        ax.add_patch(c)
    plt.show()
    """
    hsv = cv2.cvtColor(original, cv2.COLOR_RGB2HSV) / 255.0               
    saturation = hsv[:,:,1]                                                  
    darkness = np.clip(1 - hsv[:,:,2] * 1.8, 0, 1)                            
    image = np.maximum(saturation, darkness)                                 

    blobs_log = feature.blob_log(image, min_sigma=3, max_sigma=30, num_sigma=10, threshold=0.2)   
    
    # Compute radii
    blobs_log[:, 2] = blobs_log[:, 2] * (2 ** 0.5)
    
    # Display
    fig, ax = plt.subplots()
    ax.imshow(original)                                 
    for y, x, r in blobs_log:
        c = plt.Circle((x, y), r, color='red', linewidth=2, fill=False)
        ax.add_patch(c)
    plt.show()
    """
def DoG():
    image = color.rgb2gray(io.imread("polka_dots_3.jpg"))
    blobs_dog = feature.blob_dog(image, max_sigma=30, threshold=0.1)
    
    # Compute radii
    blobs_dog[:, 2] = blobs_dog[:, 2] * (2 ** 0.5)
    
    # Display
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray')
    for y, x, r in blobs_dog:
        c = plt.Circle((x, y), r, color='lime', linewidth=2, fill=False)
        ax.add_patch(c)
    plt.show()

def DoH():
    image = color.rgb2gray(io.imread("polka_dots_3.jpg"))
    blobs_doh = feature.blob_doh(image, max_sigma=30, threshold=0.01)
    
    # Display
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray')
    for y, x, r in blobs_doh:
        c = plt.Circle((x, y), r, color='blue', linewidth=2, fill=False)
        ax.add_patch(c)
    plt.show()

LoG()
DoG()
DoH()