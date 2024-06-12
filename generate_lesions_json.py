import numpy as np
import nibabel as nib
import json
import os

def generate_lesions_json(nii_file):
    # 加载NII数据
    mask_img = nib.load('Processed_Data/3d_nii_mask_files/' + nii_file)
    mask_data = mask_img.get_fdata()

    dirname = 'Processed_Data/lesions_json'
    os.makedirs(dirname, exist_ok=True)

    json_file_name = f'lesions_{nii_file[:-4]}.json'
    json_file_path = os.path.join(dirname, json_file_name)

    # 病灶区域
    lesions_slices = []

    # 遍历每一层
    for i in range(mask_data.shape[2]):
        if np.any(mask_data[:, :, i] == 3):
            lesions_slices.append(int(i))

    # 将病灶层索引写入JSON文件
    with open(json_file_path, 'w') as json_file:
        json.dump({'lesions_slices': lesions_slices}, json_file, indent=4)

    print(f'Lesions information saved to {json_file_path}')


if __name__ == '__main__':
    # 示例调用
    generate_lesions_json('study_001.nii')
