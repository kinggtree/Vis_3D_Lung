import nibabel as nib
import matplotlib.pyplot as plt
import os

patient_index = 1

filename = f'processed_study_00{patient_index}.nii'
dirname = f'patient_gray_{patient_index}'
os.makedirs(dirname)
# 加载NII数据
nii_data = nib.load('Data/'+filename)
ct_data = nii_data.get_fdata()

# 分割层
for layer_index in range(ct_data.shape[2]):
    slice_data=ct_data[:, :, layer_index]
    plt.imshow(slice_data, cmap='gray')
    plt.axis('off') # 去掉坐标轴
    plt.title('Layer {}'.format(layer_index+1))
    plt.savefig(f'{dirname}/layer{layer_index+1}.jpg', bbox_inches='tight')
