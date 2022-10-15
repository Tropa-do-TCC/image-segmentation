import os
import time
import numpy as np
import dicomHandler as dicomHandler
import wspMultithreshold as wspMultithreshold

input_dir = "results/2EFVJVCN"

bio_algorithms = ['FFA', 'KH', 'CS', 'ABC', 'EHO']
q_values = np.linspace(-2, 2, num=41)
dimension = [1,2,3,4,5]

def segmentate(image_folder, algorithm, dimension, q):

    output_dir_big = input_dir + f"-BigReg-{algorithm}-d{dimension}-q{q}"
    output_dir_high = input_dir + f"-HighIntensity-{algorithm}-d{dimension}-q{q}"
    
    os.mkdir(output_dir_big)
    os.mkdir(output_dir_high)

    for file in os.listdir(image_folder):
        dcm_path = image_folder + '/' + file

        dicom_image, pixel_array = dicomHandler.read_dicom_image(dcm_path)

        hu_image = dicomHandler.transform_to_hu(dicom_image, pixel_array)

        hist, bin_edges, best_thresholds, img_thres = wspMultithreshold.wspMultithreshold(hu_image, algorithm, dimension, q)

        high_intensity = wspMultithreshold.get_high_intensity_pixels(img_thres)

        pixel_array = dicomHandler.transform_to_pixel_array(
            dicom_image, high_intensity)

        hard_tissue = wspMultithreshold.get_largest_region(pixel_array)

        dicomHandler.save_dicom(dicom_image, pixel_array, f'{output_dir_high}/{file}')
        dicomHandler.save_dicom(dicom_image, hard_tissue, f'{output_dir_high}/{file}')

    return