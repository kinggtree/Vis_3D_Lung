import numpy as np
import nibabel as nib
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 加载NII数据
nii_data = nib.load('Data/study_001.nii')
ct_data = nii_data.get_fdata()

# 分割每个CT层
num_slices = ct_data.shape[2]

# 对每个CT层进行亮度聚类
num_clusters = 3  # 你可以根据需要调整聚类簇的数量

# for i in range(num_slices):
# 获取当前层数据
i = 20
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

# 可视化聚类结果
plt.imshow(clustered_slice_data, cmap='viridis')
plt.colorbar()
plt.title('Clustered Slice {}'.format(i+1))
plt.show()



# 假设聚类结果保存在clustered_slice_data中

# 定义最低亮度簇和次低亮度簇的标签
lowest_brightness_label = 0  # 假设最低亮度簇的标签为0
next_lowest_brightness_label = 1  # 假设次低亮度簇的标签为1

# # 遍历每个CT层
# for i in range(num_slices):
#     # 获取当前层的聚类结果
#     clustered_slice_data = ...  # 从你的数据中获取当前层的聚类结果
    
# 寻找次低亮度簇的边界
boundary_pixels = []
for x in range(clustered_slice_data.shape[0]):
    for y in range(clustered_slice_data.shape[1]):
        if clustered_slice_data[x, y] == next_lowest_brightness_label:
            # 如果像素属于次低亮度簇，则检查其周围像素
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < clustered_slice_data.shape[0] and 0 <= ny < clustered_slice_data.shape[1]:
                        if clustered_slice_data[nx, ny] != next_lowest_brightness_label:
                            boundary_pixels.append((x, y))
                            break

# 删除处于边界外的像素数据
boundary_pixels_set = set(boundary_pixels)
for x in range(clustered_slice_data.shape[0]):
    for y in range(clustered_slice_data.shape[1]):
        if (x, y) not in boundary_pixels_set:
            clustered_slice_data[x, y] = -1  # 将边界外的像素标记为-1，以便后续处理

# 输出或者处理带有边界的数据
print("Clustered slice {} with boundary pixels:".format(i+1))
print(clustered_slice_data.shape)
