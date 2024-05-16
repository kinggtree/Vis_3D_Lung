import nibabel as nib
import cv2
import numpy as np

# 读取NIfTI文件
nii_img = nib.load('Data/study_001.nii')

# 获取NIfTI数据
nii_data = nii_img.get_fdata()

nii_data11 = nii_data[:, :, 10]

# 将数据转换为与cv2.imread兼容的形式
# 可能需要根据需要进行进一步的处理，比如归一化、转换数据类型等
nii_data11 = np.array(nii_data11, dtype=np.uint8)  # 将数据类型转换为uint8

# 如果需要，可以对数据进行调整
# 比如你可能需要将数据重新排列为 (height, width, channels) 的形式
# 这取决于你的NIfTI数据的原始形状
gray_color_mapped_image = cv2.applyColorMap(nii_data11, cv2.COLORMAP_JET)

# 现在，你可以将数据传递给cv2.imread函数进行进一步处理
# 例如，如果你想要显示图像，你可以这样做：
cv2.imshow('NIfTI Image', nii_data11)
cv2.waitKey(0)
cv2.destroyAllWindows()
