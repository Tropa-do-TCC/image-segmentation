# %%
import cv2
import matplotlib.pyplot as plt
import importlib
import os

import dicomHandler
import wspMultithreshold
import plotGraph
# %%
bio_algorithms = ['FFA', 'KH', 'CS', 'ABC', 'EHO']

def main(image, algorithm, dimension, q):
    dicom_image, pixel_array = dicomHandler.read_dicom_image(image)

    original_image = pixel_array.copy()

    hu_image = dicomHandler.transform_to_hu(dicom_image, pixel_array)

    hist, bin_edges, best_thresholds, img_thres = wspMultithreshold.wspMultithreshold(
        hu_image, algorithm, dimension, q)

    plotGraph.plot_image_histogram(hu_image, hist, bin_edges)

    high_intensity = wspMultithreshold.get_high_intensity_pixels(img_thres)

    pixel_array = dicomHandler.transform_to_pixel_array(
        dicom_image, high_intensity)

    hard_tissue = wspMultithreshold.get_largests_regions(
        pixel_array, original_image)

    #dicomHandler.save_dicom(dicom_image, pixel_array,"images/temp.dcm")

    plotGraph.plot_image_histogram_threshold(
        img_thres, hist, bin_edges, best_thresholds)

    dicomHandler.show_dicom_image(high_intensity)
    dicomHandler.show_dicom_image(hard_tissue)


if __name__ == '__main__':
    image = "../Database/I1680000"
    algorithm = 'FFA'
    dimension = 2
    q = 1

    main(image, algorithm, dimension, q)