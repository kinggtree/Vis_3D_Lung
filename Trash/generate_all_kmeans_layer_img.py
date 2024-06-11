import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os

def generate_all_kmeans_layer_img(nii_file):
    filename = f'processed_{nii_file}.nii'
    dirname = f'Processed_Data/kmeans_image/kmeans_{nii_file}'
    os.makedirs(dirname, exist_ok=True)
    # 加载NII数据
    nii_data = nib.load('Processed_Data/nii_files/'+filename)
    ct_data = nii_data.get_fdata()

    # 分割层
    for layer_index in range(ct_data.shape[2]):
        slice_data=ct_data[:, :, layer_index]
        #### 原图 ####
        # plt.imshow(slice_data, cmap='gray')
        # plt.colorbar()
        # plt.title('Slice {}'.format(layer_index+1))
        # plt.tight_layout()
        # plt.show()

        #### 提取聚类后图像

        normalized_slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data))
        flattened_slice_data = normalized_slice_data.flatten()
        flattened_slice_data = np.nan_to_num(flattened_slice_data, nan=0)
        kmeans = KMeans(n_clusters=3, n_init='auto', random_state=0)
        kmeans.fit(flattened_slice_data.reshape(-1, 1))
        labels = kmeans.labels_
        clustered_slice_data = labels.reshape(normalized_slice_data.shape)
        # filtered_slice_data = np.where(clustered_slice_data == 2, 0, clustered_slice_data)

        plt.imshow(clustered_slice_data, cmap='viridis')
        plt.axis('off') # 去掉坐标轴
        plt.title('Layer {}'.format(layer_index+1))
        plt.savefig(f'{dirname}/layer{layer_index+1}.jpg', bbox_inches='tight')
        print(f'{filename} processed kmeans layer {layer_index}.')


    print(f"Finish saving {nii_file} patient kmeans img file.")

if __name__=="__main__":
    nii_file = 'study_001'
    generate_all_kmeans_layer_img(nii_file)