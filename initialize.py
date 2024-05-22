from multiprocessing import Pool
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

def process_file(nii_file):
    current_index = get_last_character(nii_file)
    start_time = time.time()
    generate_all_spilted_nii(nii_file)
    generate_all_gray_layer_img(nii_file[:-4])
    generate_all_kmeans_layer_img(nii_file[:-4])
    generate_model_html(nii_file[:-4])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Finish processing patient No.{current_index}. Time elapsed: {elapsed_time:.2f} seconds.")
    return elapsed_time

with Pool(processes=len(nii_files)) as pool:
    elapsed_times = list(tqdm(pool.imap(process_file, nii_files), total=len(nii_files), desc="Processing", unit="file"))


print('Finish processing all files!')
