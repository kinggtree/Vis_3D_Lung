import numpy as np
import cv2
from sklearn.cluster import KMeans
from skimage import morphology, measure
import nibabel as nib
import matplotlib.pyplot as plt


# 读取nii数据
def read_nii(file_path):
    image = nib.load(file_path)
    array = image.get_fdata()
    return array


# 图像二值化
def image_binarization(image):
    # 数值分布标准化
    mean = np.mean(image)
    std = np.std(image)
    image = image - mean
    image = image / std

    # 将图片最大值和最小值替换为肺部大致均值，使得图像灰度值分布均匀些，让聚类结果更可靠
    max = np.max(image)
    min = np.min(image)
    image[image == max] = mean
    image[image == min] = mean

    # 进行KMeans聚类
    kmeans = KMeans(n_clusters=2, n_init=10)
    flattened_image = image.flatten().reshape(-1, 1)
    kmeans.fit(flattened_image)
    thresholds = np.sort(kmeans.cluster_centers_.flatten())
    
    # 使用阈值进行二值化
    binary_image = np.where(image < thresholds[1], 0, 255).astype(np.uint8)
    
    return binary_image

# 腐蚀和膨胀操作
def morphology_operations(binary_image):
    kernel_erosion = np.ones((5, 5), np.uint8)      # 腐蚀算子
    kernel_dilation = np.ones((23, 23))         # 膨胀算子
    # 先腐蚀后膨胀
    eroded_image = cv2.erode(binary_image, kernel_erosion, iterations=1)
    dilated_image = cv2.dilate(eroded_image, kernel_dilation, iterations=1)
    return dilated_image

# 提取肺部mask
def extract_lung_mask(dilated_image):
    # 使用连通区域标签
    labeled_image = measure.label(dilated_image)
    lung_region = None
    max_area = 0
    
    # 找到最大的连通区域作为肺部区域
    for region in measure.regionprops(labeled_image):
        if region.area > max_area:
            max_area = region.area
            lung_region = region
    
    lung_mask = np.zeros_like(dilated_image)
    lung_mask[labeled_image == lung_region.label] = 1

     # 进行膨胀操作以填充并扩张肺部区域
    kernel = np.ones((5, 5), np.uint8)
    lung_mask = cv2.dilate(lung_mask.astype(np.uint8), kernel, iterations=1)
    
    return lung_mask

# 读取nii数据
nii_data = read_nii("Data/study_001.nii")

lung_masks = []
# 对每个层面的数据进行处理
for i in range(nii_data.shape[2]):
    image = nii_data[:, :, i]
    # 图像二值化
    binary_image = image_binarization(image)
    # 腐蚀和膨胀操作
    dilated_image = morphology_operations(binary_image)
    # 提取肺部mask
    lung_mask = extract_lung_mask(dilated_image)
    lung_masks.append(lung_mask)
    print("\nLayer", i+1, "finish.\n")

# lung_masks现在包含了每个层面的肺部mask


# 获取第11个组的肺部mask
lung_mask = lung_masks[10]

# 显示肺部mask图像
plt.imshow(lung_mask, cmap='gray')
plt.title('Lung Mask')
plt.axis('off')
plt.show()
