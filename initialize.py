from multiprocessing import Pool
from generate_model_html import generate_model_html
import os
import glob
from tqdm import tqdm
import time
from generate_gray_img import generate_gray_img
from generate_masked_img import generate_masked_img

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
    'Processed_Data/nii_mask_files',
    'Processed_Data/3D_model',
    'Processed_Data/masked_img',
    'Processed_Data/gray_image'
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

folder_path = 'Data'
nii_files = get_nii_files(folder_path)

# 获取当前脚本所在的目录
current_directory = os.path.dirname(os.path.abspath(__name__))
original_nii_dict = os.path.join(current_directory, folder_path)
mask_nii_dict = os.path.join(folder_path, folders[1])

def process_file(nii_file):
    current_index = get_last_character(nii_file)
    start_time = time.time()

    # 添加使用nnUNet来提取mask的部分

    generate_gray_img(nii_file)
    generate_masked_img(nii_file)

    generate_model_html(nii_file)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Finish processing patient No.{current_index}. Time elapsed: {elapsed_time:.2f} seconds.")
    return elapsed_time

# # 调试用
# process_file(nii_files[0])

with Pool(processes=len(nii_files)) as pool:
    elapsed_times = list(tqdm(pool.imap(process_file, nii_files), total=len(nii_files), desc="Processing", unit="file"))


print('Finish processing all files!')
