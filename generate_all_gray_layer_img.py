import nibabel as nib
import matplotlib.pyplot as plt
import os

def generate_all_gray_layer_img(nii_file):
    filename = f'processed_{nii_file}.nii'
    dirname = f'Processed_Data/gray_image/gray_{nii_file}'
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

    print(f"Finish saving {nii_file} patient gray img file.")


if __name__=="__main__":
    nii_file = 'study_001'
    generate_all_gray_layer_img(nii_file)
