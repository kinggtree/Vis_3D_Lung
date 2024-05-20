from generate_all_gray_layer_img import generate_all_gray_layer_img
from generate_all_kmeans_layer_img import generate_all_kmeans_layer_img
from generate_all_spilted_nii import generate_all_spilted_nii
from generate_model_html import generate_model_html
import os
import glob
from tqdm import tqdm
import time

def get_last_character(file_path):
    filename = os.path.basename(file_path)
    filename_without_extension = os.path.splitext(filename)[0]  # 获取文件名（不含扩展名）
    last_character = filename_without_extension[-1]  # 获取最后一个字符
    return last_character

def get_nii_files(folder_path):
    nii_files = []
    for file_path in glob.glob(os.path.join(folder_path, '*.nii')):
        if 'processed' not in file_path:
            nii_files.append(os.path.basename(file_path))
    return nii_files

folders = [
    'Processed_Data',
    'Processed_Data/nii_files',
    'Processed_Data/gray_image',
    'Processed_Data/kmeans_image',
    'Processed_Data/3D_model'
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

folder_path = 'Data'
nii_files = get_nii_files(folder_path)

remaining_files = len(nii_files)
total_estimated_time = 0

for nii_file in tqdm(nii_files, desc="Processing", unit="file"):
    current_index = get_last_character(nii_file)
    start_time = time.time()
    generate_all_spilted_nii(nii_file)
    generate_all_gray_layer_img(current_index)
    generate_all_kmeans_layer_img(current_index)
    generate_model_html(current_index)
    end_time = time.time()
    elapsed_time = end_time - start_time
    total_estimated_time += elapsed_time * remaining_files
    remaining_files -= 1
    print(f"Finish processing patient No.{current_index}. Time elapsed: {elapsed_time:.2f} seconds.")
    print(f"Estimated time remaining: {total_estimated_time:.2f} seconds.")
    
print('Finish processing all files!')
