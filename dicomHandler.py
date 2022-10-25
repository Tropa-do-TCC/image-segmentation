# %%
import matplotlib.pyplot as plt
from pydicom import dcmread
import os
import numpy as np
from pydicom.pixel_data_handlers.util import apply_modality_lut

# %%


def image_transformation(pixel_array):
    upper_bound = int(pixel_array.max())
    c = 1
    b = 1.3

    transformed = pixel_array**b
    max_val = transformed.max()
    output_img = (transformed/max_val)*upper_bound

    return output_img.astype(np.uint16)
    # return transformed

# %%


def transform_to_hu(medical_image, image):
    intercept = medical_image.RescaleIntercept
    slope = medical_image.RescaleSlope
    hu_image = image * slope + intercept

    return hu_image

# %%


def transform_to_pixel_array(medical_image, hu_image):
    intercept = medical_image.RescaleIntercept
    slope = medical_image.RescaleSlope
    image = (hu_image - intercept)/slope

    return image.astype(np.int16)

# %%


def show_dicom_image(med_img, title=""):
    plt.figure(figsize=(15, 7))
    plt.imshow(med_img, cmap='gray')
    plt.title(title)
    plt.axis('off')

# %%


def read_dicom_image(file_path):
    medical_image = dcmread(file_path)
    pixel_array = medical_image.pixel_array
    return medical_image, pixel_array

# %%


def save_dicom(dicom, new_image, file_path):
    dicom.PixelData = new_image.tobytes()
    dicom.save_as(file_path)
