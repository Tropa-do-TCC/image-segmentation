import os
import time
import numpy as np
import dicomHandler as dicomHandler
import wspMultithreshold as wspMultithreshold
import concurrent.futures

input_dir = "results/2EFVJVCN"

all_slices = os.listdir(input_dir)

bio_algorithms = ['FFA', 'KH', 'CS', 'ABC', 'EHO']
q_values = np.linspace(-2, 2, num=41)
dimension = [1,2,3,4,5]

output_dir_high = ""
output_dir_big = ""
current_bio = ""
current_dim = 0
current_q = 0

def segment_slice(dcm_file_path):
    dicom_img = input_dir + '/' + dcm_file_path
    
    dicom_image, pixel_array = dicomHandler.read_dicom_image(dicom_img)

    hu_image = dicomHandler.transform_to_hu(dicom_image, pixel_array)

    hist, bin_edges, best_thresholds, img_thres = wspMultithreshold.wspMultithreshold(hu_image, current_bio, current_dim, current_q)

    high_intensity = wspMultithreshold.get_high_intensity_pixels(img_thres)

    pixel_array = dicomHandler.transform_to_pixel_array(dicom_image, high_intensity)

    hard_tissue = wspMultithreshold.get_largest_region(pixel_array)

    dicomHandler.save_dicom(dicom_image, pixel_array, f'{output_dir_high}/{dcm_file_path}')
    dicomHandler.save_dicom(dicom_image, hard_tissue, f'{output_dir_big}/{dcm_file_path}')


for dim in dimension:
    for bio in bio_algorithms:
        for q_v in q_values:
            current_bio = bio
            current_dim = dim
            current_q = q_v
            output_dir_big = input_dir + f"-BigReg-{bio}-d{dim}-q{q_v}"
            output_dir_high = input_dir + f"-HighIntensity-{bio}-d{dim}-q{q_v}" 
            os.mkdir(output_dir_big)
            os.mkdir(output_dir_high)

            with concurrent.futures.ProcessPoolExecutor() as executor:
                executor.map(segment_slice, all_slices)