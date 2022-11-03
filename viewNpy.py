import os
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

def plot_image_histogram(img, img2):
    plt.figure(figsize=(15, 5)) 
    plt.subplot(1,2,1)
    plt.imshow(img,cmap='gray')
    plt.title('original')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1,2,2)
    plt.imshow(img2,cmap='gray')
    plt.title('segmented')
    plt.xticks([])
    plt.yticks([])

    plt.show()

org_output_dir = "Dataset/UsevillaBone/original/"
seg_output_dir = "Dataset/UsevillaBone/segmented/"
our_output_dir = "Results/Test-HighIntensity-FFA-d1-q1/"

all_images = []

for file in os.listdir(our_output_dir):
    all_images.append(file)

for index in range(len(all_images)):
    data = np.load(org_output_dir + '/' + all_images[index])
    data_seg = np.load(our_output_dir + '/' + all_images[index])
    plot_image_histogram(data, data_seg)