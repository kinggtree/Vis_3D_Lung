import nibabel as nib
import numpy as np
import scipy.ndimage as ndi
import pyvista as pv
from skimage import measure


index = 1

# 加载nii数据
ct_image = nib.load(f'Data/processed_study_00{index}.nii')
ct_data = ct_image.get_fdata()

# 定义阈值，通常肺部区域的像素值较低
threshold = -1000

# 阈值分割
lung_mask = ct_data > threshold

# 进行连通区域分析
labels, num_features = ndi.label(lung_mask)

# 保留较大的连通区域
sizes = ndi.sum(lung_mask, labels, range(num_features + 1))
mask_size = sizes < 500  # 去除小于500像素的区域，这个值可以调整
remove_pixel = mask_size[labels]
labels[remove_pixel] = 0

# 生成清理后的掩码
cleaned_lung_mask = labels > 0

# 应用掩码提取肺部
lung_extracted = ct_data * cleaned_lung_mask

# 将3D numpy数组转换为pyvista的UnstructuredGrid对象，添加层间距离
def numpy_to_pyvista(vol, slice_spacing=1.0):
    verts, faces, _, _ = measure.marching_cubes(vol, level=-300)
    
    # 调整顶点位置，增加层间距离
    verts[:, 2] *= slice_spacing
    
    faces = np.hstack([np.full((faces.shape[0], 1), 3), faces]).astype(np.int64)
    grid = pv.PolyData(verts, faces)
    return grid

# 设置层间距离，例如每层之间的距离设为2.0
slice_spacing = 10.0

# 提取肺部区域
lung_grid = numpy_to_pyvista(lung_extracted, slice_spacing)

# 创建一个Plotter对象进行3D展示
plotter = pv.Plotter()
plotter.add_mesh(lung_grid, color='white', opacity=0.5)
# plotter.add_axes()

plotter.export_html(f'3d_model_{index}.html')
