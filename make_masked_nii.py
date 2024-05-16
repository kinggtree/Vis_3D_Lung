import numpy as np
import nibabel as nib
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from skimage.segmentation import find_boundaries
from scipy.ndimage import binary_fill_holes, binary_erosion, binary_dilation


filename = 'study_008.nii'
# 加载NII数据
nii_data = nib.load('Data/'+filename)
ct_data = nii_data.get_fdata()

# 分割每个CT层
num_slices = ct_data.shape[2]

# 对每个CT层进行亮度聚类
num_clusters = 3  # 你可以根据需要调整聚类簇的数量

processed_ct_data = np.zeros_like(ct_data)

for i in range(num_slices):
    # 获取当前层数据
    slice_data = ct_data[:, :, i]

    # 标准化数据
    normalized_slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data))

    # 将二维数据转换为一维
    flattened_slice_data = normalized_slice_data.flatten()

    # 应用K均值聚类
    kmeans = KMeans(n_clusters=num_clusters, n_init='auto', random_state=0)
    kmeans.fit(flattened_slice_data.reshape(-1, 1))

    # 获取聚类标签
    labels = kmeans.labels_

    # 将聚类标签重塑回二维形状
    clustered_slice_data = labels.reshape(normalized_slice_data.shape)

    # 查看聚类簇的索引范围
    min_index = np.min(labels)
    max_index = np.max(labels)

    # 查看唯一的聚类标签
    unique_labels = np.unique(labels)

    # 过滤标签不为1的像素
    filtered_slice_data = np.where(clustered_slice_data == 2, 0, clustered_slice_data)

    # 找到标签为2的区域边界
    boundaries = find_boundaries(filtered_slice_data, mode='outer')

    # 将边界内的所有区域填充
    filled_image = binary_fill_holes(boundaries)

    # 肺部区域（标签为2）
    lung_data_temp = np.where(clustered_slice_data == 0, 2, clustered_slice_data)

    lung_data = np.where(lung_data_temp == 1, 0, lung_data_temp)

    # 异或操作找出在人体区域内的肺部区域
    filtered_lung_data = np.logical_and(lung_data, filled_image)

    # 腐蚀操作
    eroded_image = binary_erosion(filtered_lung_data)

    # 膨胀操作
    dilated_image = binary_dilation(eroded_image)

    # 将边界内的所有区域填充
    filled_dilated_image = binary_fill_holes(dilated_image)

    masked_image = np.where(filled_dilated_image, slice_data, 0)

    # 将处理后的切片保存到新的数据集中
    processed_ct_data[:, :, i] = masked_image

    print("Processed", i+1, "slice.")



# 保存处理后的结果为NII文件
processed_nii = nib.Nifti1Image(processed_ct_data, nii_data.affine)
nib.save(processed_nii, 'Data/processed_'+filename)

print("Finish processing!")

