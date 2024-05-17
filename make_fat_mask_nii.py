from sklearn.cluster import KMeans
import numpy as np
import nibabel as nib

filename = 'processed_study_001.nii'
# 加载NII数据
nii_data = nib.load('Data/'+filename)
ct_data = nii_data.get_fdata()

num_slices = ct_data.shape[2]

processed_ct_data = np.zeros_like(ct_data)


for i in range(num_slices):
    # 获取当前层数据
    slice_data = ct_data[:, :, i]

    # 标准化数据
    normalized_slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data))

    # 将二维数据转换为一维
    flattened_slice_data = normalized_slice_data.flatten()

    # 加载原始数据并处理NaN值
    flattened_slice_data = np.nan_to_num(flattened_slice_data, nan=0)

    # 应用K均值聚类
    kmeans = KMeans(n_clusters=3, n_init='auto', random_state=0)
    kmeans.fit(flattened_slice_data.reshape(-1, 1))

    # 获取聚类标签
    labels = kmeans.labels_

    # 将聚类标签重塑回二维形状
    clustered_slice_data = labels.reshape(normalized_slice_data.shape)

    filtered_slice_data = np.where(clustered_slice_data == 2, 0, clustered_slice_data)

    masked_image = np.where(filtered_slice_data, slice_data, 0)

    # 将处理后的切片保存到新的数据集中
    processed_ct_data[:, :, i] = masked_image

    print(filename, "fat processed", i+1, "slice.")



# 保存处理后的结果为NII文件
processed_nii = nib.Nifti1Image(processed_ct_data, nii_data.affine)
nib.save(processed_nii, 'Data/fat_'+filename)

print("Finish processing!")