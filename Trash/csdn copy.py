import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans
from skimage import measure, morphology
import matplotlib.pyplot as plt
from skimage import io
import nibabel as nib




nii_img = nib.load('Data/study_001.nii')

# 获取NIfTI数据
nii_data = nii_img.get_fdata()

nii_data11 = nii_data[:, :, 10]

# 将数据转换为与cv2.imread兼容的形式
# 可能需要根据需要进行进一步的处理，比如归一化、转换数据类型等
img = np.array(nii_data11, dtype=np.uint8)  # 将数据类型转换为uint8

# 数值分布标准化
mean = np.mean(img)
std = np.std(img)
img = img - mean
img = img / std


# 载入图片的主要区域，用于KMeans聚类
middle = img[100:1000, 300:9000]
mean = np.mean(middle)

# 将图像中最大值和最小值的像素值归一化到均值，确保图像在均值附近分布，增强结果的可靠性
max = np.max(img)
min = np.min(img)
# print(mean, min, max)
img[img == max] = mean
img[img == min] = mean

# KMeans聚类，产生两类，一类是骨骼和血管，一类是肺部区域
kmeans = KMeans(n_clusters=3, n_init='auto').fit(np.reshape(middle, [np.prod(middle.shape), 1]))
centers = sorted(kmeans.cluster_centers_.flatten())
threshold = np.mean(centers)
thresh_img = np.where(img < threshold, 1.0, 0.0)  # 用于图像阈值化，对图像进行二值化处理，得到thresh_img
print('kmean centers:', centers)
print('threshold:', threshold)

# 腐蚀和膨胀
kernel_erosion = np.ones((5, 5))  # 腐蚀算子
kernel_dilation = np.ones((23, 23))  # 膨胀算子

# opening = cv.morphologyEx(thresh_img, cv.MORPH_OPEN, kernel)
erosion = cv.erode(thresh_img, kernel_erosion, iterations=1)
dilation = cv.dilate(erosion, kernel_dilation, iterations=1)


labels = measure.label(dilation)  # 对连通区域进行标记
regions = measure.regionprops(labels)  # 获取连通区域
# print(len(regions))

# 根据肺的lung图，设置经验值，获取肺部标签
good_labels = []
for prop in regions:
    B = prop.bbox
    # print(B)
    if B[2] - B[0] < 700 and B[3] - B[1] < 500 and B[0] > 200 and B[2] < 1000:
        good_labels.append(prop.label)

# 根据肺部标签获取肺部mask，并再次进行膨胀操作，以填满并扩张肺部区域
mask = np.ndarray([512, 512], dtype=np.int8)
mask[:] = 0
for N in good_labels:
    mask = mask + np.where(labels == N, 1, 0)
mask = morphology.dilation(mask, np.ones((10, 10)))  # one last dilation


mask_region = img * mask

# 画出分割图像
fig, ax = plt.subplots(2, 2, figsize=[10, 10])
ax[0, 0].imshow(img, cmap='gray')  # CT切片
ax[0, 0].set_title("CT source img")
ax[0, 1].imshow(labels)  # CT的初步标记
ax[0, 1].set_title("CT labels")
ax[1, 0].imshow(mask, cmap='gray')  # CT mask，标记区域均匀
ax[1, 0].set_title("CT mask")
ax[1, 1].imshow(mask_region, cmap='gray')  # 标记的肺部区域
ax[1, 1].set_title("CT mask region")

# plt.savefig('./result/result.jpg')
plt.show()


# 转为int8格式图片，所以我们在这里标记
# mask = (mask - mask.min()) / (mask.max() - mask.min()) * 255).astype(np.uint8)
# mask_region = (mask_region - mask_region.min()) / (mask_region.max() - mask_region.min()) * 255).astype(np.uint8)

# 保存图像
# io.imsave('./result/lung_shape.jpg', mask)
# io.imsave('./result/lung_mask_region.jpg', mask_region)


