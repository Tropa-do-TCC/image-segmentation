import reconstruction
import os

input_dir = "ResultsDCM"

all_slices = os.listdir(input_dir)

for sample in all_slices:
    print(sample)
    reconstruction.rec3d(input_dir + '/' + sample)