# %%
import cv2
import matplotlib.pyplot as plt
import importlib
import os
from ipywidgets import interact
from ipywidgets import interact_manual
from IPython.display import display
from ipywidgets import widgets

# %%
import ipynb.fs.full.wspFFA as wspFirefly
import ipynb.fs.full.wspCS as wspCuckooSearch
import ipynb.fs.full.wspKH as wspKrillHerd
import ipynb.fs.full.wspEHO as wspElephantHerding
import ipynb.fs.full.wspABC as wspArtificialBeeColony

import ipynb.fs.full.plotGraph as plotGraph
import ipynb.fs.full.wspMultithreshold as wspMultithreshold
import ipynb.fs.full.dicomHandler as dicomHandler

importlib.reload(wspFirefly)
importlib.reload(wspCuckooSearch)
importlib.reload(wspKrillHerd)
importlib.reload(wspElephantHerding)
importlib.reload(wspArtificialBeeColony)

importlib.reload(plotGraph)
importlib.reload(wspMultithreshold)
importlib.reload(dicomHandler)

# %%


def readImage(img_path):
    image = cv2.imread(img_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return img


# %%
bio_algorithms = ['FFA', 'KH', 'CS', 'ABC', 'EHO']

# %%
folder_dir = "images"

all_images = ["../Database/I1680000"]

for file in os.listdir(folder_dir):
    if file.endswith('.png') or file.endswith('.jpg'):
        all_images.append(file)

# %%


def main(image, algorithm, dimension, q):
    dicom_image, pixel_array = dicomHandler.read_dicom_image(image)

    hu_image = dicomHandler.transform_to_hu(dicom_image, pixel_array)

    hist, bin_edges, best_thresholds, img_thres = wspMultithreshold.wspMultithreshold(
        hu_image, algorithm, dimension, q)

    plotGraph.plot_image_histogram(hu_image, hist, bin_edges)

    high_intensity = wspMultithreshold.get_high_intensity_pixels(img_thres)

    pixel_array = dicomHandler.transform_to_pixel_array(
        dicom_image, high_intensity)

    hard_tissue = wspMultithreshold.get_largest_region(pixel_array)
    print(hard_tissue.min(), hard_tissue.max())
    print(pixel_array.min(), pixel_array.max())
    #dicomHandler.save_dicom(dicom_image, pixel_array,"images/temp.dcm")

    plotGraph.plot_image_histogram_threshold(
        img_thres, hist, bin_edges, best_thresholds)

    dicomHandler.show_dicom_image(high_intensity)
    dicomHandler.show_dicom_image(hard_tissue)


# %%
interact_manual(main, image=all_images, algorithm=bio_algorithms,
                dimension=widgets.IntSlider(min=1, max=5, step=1, value=2),
                q=widgets.FloatSlider(min=-2, max=2, step=0.1, value=1))
