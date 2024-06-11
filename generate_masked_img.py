import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os


def generate_masked_img(nii_file):
    # 加载NII数据
    ct_img = nib.load('Data/'+nii_file)
    ct_data = ct_img.get_fdata()
    mask_img = nib.load('Processed_Data/nii_mask_files/'+nii_file)
    mask_data = mask_img.get_fdata()

    dirname = f'Processed_Data/masked_img/masked_{nii_file[:-4]}'

    os.makedirs(dirname, exist_ok=True)

    # 检查层数分割每个CT层
    num_slices = ct_data.shape[2]

    for layer in range(num_slices):
        # 创建颜色映射
        cmap = plt.cm.Reds
        cmap.set_under(color='black', alpha=0)  # 设置背景为透明
        cmap.set_over(color='blue', alpha=0.5)  # 设置掩码值为1的颜色为蓝色透明
        cmap.set_over(color='green', alpha=0.5)  # 设置掩码值为2的颜色为绿色透明
        cmap.set_over(color='red', alpha=0.5)  # 设置掩码值为3的颜色为红色透明

        plt.imshow(ct_data[:, :, layer], cmap='gray')
        plt.axis('off') # 去掉坐标轴

        # 显示掩码图像的指定层，设置掩码范围
        plt.imshow(mask_data[:, :, layer], cmap=cmap, alpha=0.3, vmin=0.5, vmax=2.5)
        plt.title(f'Layer {layer}')

        plt.savefig(f'{dirname}/layer{layer+1}.jpg', bbox_inches='tight')
        print(f'{nii_file} processed masked layer {layer}.')


if __name__=="__main__":
    filename = 'study_001.nii'
    generate_masked_img(filename)