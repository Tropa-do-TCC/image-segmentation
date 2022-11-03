import os
import time
import numpy as np
import dicomHandler as dicomHandler
import wspMultithreshold as wspMultithreshold
import concurrent.futures
from itertools import repeat

input_dir = "Dataset/UsevillaBone/original"
output_dir = "Results/Test"
all_slices = os.listdir(input_dir)

bio_algorithms = ['FFA']#, 'KH', 'CS', 'ABC', 'EHO']
q_values = [1]
dimension = [1,2,3]
transform_values = [1.3, 1.7]


def segment_slice(dcm_file_path, current_bio, current_dim, current_q, output_dir_big, output_dir_high):
    dicom_img = input_dir + '/' + dcm_file_path
    
    pixel_array = dicomHandler.read_npy_image(dicom_img)

    transformed_pixel_array = dicomHandler.image_transformation(pixel_array)

    original_image = pixel_array.copy()

    hu_image = dicomHandler.transform_npy_to_hu(transformed_pixel_array)

    hist, bin_edges, best_thresholds, img_thres = wspMultithreshold.wspMultithreshold(hu_image, current_bio, current_dim, current_q)

    high_intensity = wspMultithreshold.get_high_intensity_pixels(img_thres)

    pixel_array = dicomHandler.transform_to_npy_pixel_array(high_intensity)

    hard_tissue = wspMultithreshold.get_largests_regions(pixel_array, original_image)

    dicomHandler.save_npy(pixel_array, f'{output_dir_high}/{dcm_file_path}')
    dicomHandler.save_npy(hard_tissue, f'{output_dir_big}/{dcm_file_path}')

    return


def main():
    for dim in dimension:
        for bio in bio_algorithms:
            for q_v in q_values:
                current_bio = bio
                current_dim = dim
                current_q = q_v
                output_dir_big = output_dir + f"-BigReg-{bio}-d{dim}-q{q_v}"
                output_dir_high = output_dir + f"-HighIntensity-{bio}-d{dim}-q{q_v}" 
                os.mkdir(output_dir_big)
                os.mkdir(output_dir_high)

                with concurrent.futures.ProcessPoolExecutor() as executor:
                    executor.map(segment_slice, all_slices, repeat(current_bio), repeat(current_dim), repeat(current_q), repeat(output_dir_big), repeat(output_dir_high))

                print(f'Done: {bio}-d{dim}-q{q_v}')

if __name__ == '__main__':
    main()