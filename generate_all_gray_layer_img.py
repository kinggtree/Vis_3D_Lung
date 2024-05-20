import nibabel as nib
import matplotlib.pyplot as plt
import os

def generate_all_gray_layer_img(patient_index):
    filename = f'processed_study_00{patient_index}.nii'
    dirname = f'Processed_Data/gray_image/patient_gray_{patient_index}'
    os.makedirs(dirname, exist_ok=True)
    # 加载NII数据
    nii_data = nib.load('Processed_Data/nii_files/'+filename)
    ct_data = nii_data.get_fdata()

    # 分割层
    for layer_index in range(ct_data.shape[2]):
        slice_data=ct_data[:, :, layer_index]
        plt.imshow(slice_data, cmap='gray')
        plt.axis('off') # 去掉坐标轴
        plt.title('Layer {}'.format(layer_index+1))
        plt.savefig(f'{dirname}/layer{layer_index+1}.jpg', bbox_inches='tight')
        print(f'{filename} processed gray layer {layer_index}.')

    print(f"Finish saving No.{patient_index} patient gray img file.")
