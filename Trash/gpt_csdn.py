import numpy as np
import cv2
from sklearn.cluster import KMeans
from skimage import measure, morphology
import matplotlib.pyplot as plt
import nibabel as nib

# 读取NIfTI数据
nii_file = 'Data/study_001.nii'
nii_data = nib.load(nii_file)
img = nii_data.get_fdata()[:, :, 10]

# 数值分布标准化
mean = np.mean(img)
std = np.std(img)
img = img - mean
img = img / std

# 取中间层作为聚类的输入
middle_slice = img# [:, :, img.shape[2] // 2]

# KMeans聚类，产生两类，一类是骨骼和血管，一类是肺部区域
kmeans = KMeans(n_clusters=2, n_init='auto').fit(np.reshape(middle_slice, [-1, 1]))
centers = sorted(kmeans.cluster_centers_.flatten())
threshold = np.mean(centers)
thresh_img = np.where(img < threshold, 1.0, 0.0)

# 腐蚀和膨胀
kernel_erosion = np.ones((5, 5))
kernel_dilation = np.ones((23, 23))

erosion = cv2.erode(thresh_img, kernel_erosion, iterations=1)
dilation = cv2.dilate(erosion, kernel_dilation, iterations=1)

labels = measure.label(dilation)
regions = measure.regionprops(labels)

good_labels = []
for prop in regions:
    bbox = prop.bbox
    if bbox[2] - bbox[0] < 700 and bbox[3] - bbox[1] < 500 and bbox[0] > 200 and bbox[2] < 1000:
        good_labels.append(prop.label)

mask = np.zeros_like(labels)
for label in good_labels:
    mask = np.where(labels == label, 1, 0) | mask

mask = morphology.dilation(mask, np.ones((10, 10)))

mask_region = img * mask

# 画出分割图像
fig, ax = plt.subplots(2, 2, figsize=[10, 10])
ax[0, 0].imshow(middle_slice, cmap='gray')  # 中间层切片
ax[0, 0].set_title("Middle CT slice")
ax[0, 1].imshow(labels)  # 初步标记
ax[0, 1].set_title("Initial labels")
ax[1, 0].imshow(mask, cmap='gray')  # 肺部 mask
ax[1, 0].set_title("Lung mask")
ax[1, 1].imshow(mask_region, cmap='gray')  # 标记的肺部区域
ax[1, 1].set_title("Lung mask region")

plt.show()
