import os
import time
import numpy as np
import dicomHandler as dicomHandler
import wspMultithreshold as wspMultithreshold
import concurrent.futures
from itertools import repeat
import cv2

input_dir = "Dataset/UsevillaBone/original"
output_dir = "Results/"
all_slices = os.listdir(input_dir)

bio_algorithms = ['FFA', 'KH', 'CS', 'ABC', 'EHO']

q_values = np.arange(-1,1.1, 0.1)
q_values = [int(x) if x.is_integer() else np.around(x, decimals=1) for x in np.around(q_values, decimals=1)]

dimension = [1,2,3,4,5]
transform_values = [1, 1.3, 1.5, 1.7]
gau_values = [3,5]

def segment_slice(dcm_file_path, current_bio, current_dim, current_q, t_val, kernel, output_dir_big, output_dir_high):
    dicom_img = input_dir + '/' + dcm_file_path
    
    pixel_array = dicomHandler.read_npy_image(dicom_img)

    blur = cv2.GaussianBlur(pixel_array, (kernel,kernel), 0)

    transformed_pixel_array = dicomHandler.image_transformation(blur, t_val)

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
                for t_v in transform_values:
                    for k_v in gau_values:
                        current_bio = bio
                        current_dim = dim
                        current_q = q_v
                        current_t = t_v
                        current_kernel = k_v
                        output_dir_big = output_dir + f"BigReg_{bio}_d{dim}_q{q_v}_t{t_v}"
                        output_dir_high = output_dir + f"HighIntensity_{bio}_d{dim}_q{q_v}_t{t_v}"

                        if not os.path.exists(output_dir_big):
                            os.mkdir(output_dir_big)
                        if not os.path.exists(output_dir_high):
                            os.mkdir(output_dir_high)

                        with concurrent.futures.ProcessPoolExecutor() as executor:
                            executor.map(segment_slice, all_slices, repeat(current_bio), repeat(current_dim), repeat(current_q), repeat(current_t), repeat(current_kernel), repeat(output_dir_big), repeat(output_dir_high))

                        print(f'Done: {bio}-d{dim}-q{q_v}-t{t_v}-k{k_v}')

if __name__ == '__main__':
    main()