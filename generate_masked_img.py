import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import json


def read_lesions_json(json_file_path):
    # 打开并读取JSON文件
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # 提取病灶层数信息
    lesions_slices = data.get('lesions_slices', [])

    return lesions_slices

def generate_masked_img(nii_file):
    # 读取CT图像
    ct_img = nib.load('Data/' + nii_file)
    ct_data = ct_img.get_fdata()

    # 读取肺部区域掩码和病灶区域掩码
    lung_mask_img = nib.load('Processed_Data/2d_nii_mask_files/' + nii_file)
    # lesions_mask_img = nib.load('Processed_Data/3d_nii_mask_files/' + nii_file)
    # lung_mask_data = lung_mask_img.get_fdata()
    # lesions_mask_data = lesions_mask_img.get_fdata()

    # # 读取病灶层数信息
    # lesions_slices = read_lesions_json(f'Processed_Data/lesions_json/lesions_{nii_file[:-4]}.json')

    # # 创建叠加后的掩码
    # mask_data = np.copy(lung_mask_data)

    # # 将病灶掩码中的label为3的部分叠加到肺部掩码中
    # for slice_idx in lesions_slices:
    #     mask_data[:, :, slice_idx][lesions_mask_data[:, :, slice_idx] == 3] = 3
    mask_data = lung_mask_img.get_fdata()

    dirname = f'Processed_Data/masked_img/masked_{nii_file[:-4]}'

    os.makedirs(dirname, exist_ok=True)

    # 定义自定义颜色映射，包括黑色背景
    cmap = mcolors.ListedColormap(['black', 'blue', 'green', 'red'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # 检查层数分割每个CT层
    num_slices = ct_data.shape[2]

    for layer in range(num_slices):
        if np.max(mask_data[:, :, layer]) == 0:
            continue

        plt.imshow(ct_data[:, :, layer], cmap='gray')
        plt.axis('off')  # 去掉坐标轴

        # 显示掩码图像的指定层，设置掩码范围
        plt.imshow(mask_data[:, :, layer], cmap=cmap, norm=norm, alpha=0.3)
        plt.title(f'Layer {layer+1}')

        plt.savefig(f'{dirname}/layer{layer+1}.jpg', bbox_inches='tight')
        plt.close()
        print(f'{nii_file} processed masked layer {layer}.')


if __name__ == "__main__":
    filename = 'study_001.nii'
    generate_masked_img(filename)
