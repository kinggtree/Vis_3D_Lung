import nibabel as nib
import numpy as np
import scipy.ndimage as ndi
import pyvista as pv
from skimage import measure
import json


def read_lesions_json(json_file_path):
    # 打开并读取JSON文件
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # 提取病灶层数信息
    lesions_slices = data.get('lesions_slices', [])

    return lesions_slices

# 将3D numpy数组转换为pyvista的UnstructuredGrid对象，添加层间距离，并增加Marching Cubes的Level

# 高精度版
# def numpy_to_pyvista(vol, slice_spacing=1.0, level=-300):
#     verts, faces, _, _ = measure.marching_cubes(vol, level=level)
    
#     # 调整顶点位置，增加层间距离
#     verts[:, 2] *= slice_spacing
    
#     faces = np.hstack([np.full((faces.shape[0], 1), 3), faces]).astype(np.int64)
#     grid = pv.PolyData(verts, faces)
#     return grid

# 低精度版
def numpy_to_pyvista(vol, slice_spacing=1.0, level=-300, reduce_factor=2):
    # 降采样
    vol = ndi.zoom(vol, (1/reduce_factor, 1/reduce_factor, 1/reduce_factor), order=1)

    verts, faces, _, _ = measure.marching_cubes(vol, level=level)
    
    # 调整顶点位置，增加层间距离
    verts[:, 2] *= slice_spacing
    
    faces = np.hstack([np.full((faces.shape[0], 1), 3), faces]).astype(np.int64)
    grid = pv.PolyData(verts, faces)
    
    # 简化网格
    grid = grid.decimate_pro(0.5)  # 0.5 表示简化到50%的面数
    
    return grid

def generate_model_html(nii_file):
    print(f'Generating {nii_file} patient 3D model...')
    # 读取CT图像
    ct_img = nib.load('Data/' + nii_file)
    ct_data = ct_img.get_fdata()

    # 读取肺部区域掩码和病灶区域掩码
    lung_mask_img = nib.load('Processed_Data/2d_nii_mask_files/' + nii_file)
    # lesions_mask_img = nib.load('Processed_Data/3d_nii_mask_files/' + nii_file)
    # lung_mask_data = lung_mask_img.get_fdata()
    # lesions_mask_data = lesions_mask_img.get_fdata()

    # # 读取病灶层数信息
    # lesions_slices = read_lesions_json(f'Processed_Data/lesions_json/lesions_{nii_file[:-4]}.json')

    # # 创建叠加后的掩码
    # mask_data = np.copy(lung_mask_data)

    # # 将病灶掩码中的label为3的部分叠加到肺部掩码中
    # for slice_idx in lesions_slices:
    #     mask_data[:, :, slice_idx][lesions_mask_data[:, :, slice_idx] == 3] = 3
    mask_data = lung_mask_img.get_fdata()

    # 肺部区域
    lung_mask = np.zeros_like(mask_data)
    lung_mask[mask_data == 1] = 1
    lung_mask[mask_data == 2] = 1

    # 去除空的层
    non_empty_slices = np.any(lung_mask, axis=(0, 1))
    ct_data = ct_data[:, :, non_empty_slices]
    lung_mask = lung_mask[:, :, non_empty_slices]

    # 应用掩码提取肺部
    lung_extracted = ct_data * lung_mask

    # 设置层间距离，例如每层之间的距离设为10.0，以及Marching Cubes的Level
    slice_spacing = 10.0
    level = -500  # 适当调整level的值

    # 提取肺部区域
    lung_grid = numpy_to_pyvista(lung_extracted, slice_spacing, level)

    # 创建一个Plotter对象进行3D展示
    plotter = pv.Plotter()
    plotter.add_mesh(lung_grid.smooth(n_iter=100), color='white', opacity=0.5)  # 应用平滑算法

    # 新冠感染区域
    if(np.max(mask_data) == 3):
        covid_mask = np.where(mask_data == 3, mask_data, 0)
        # 去除空的层
        covid_mask = covid_mask[:, :, non_empty_slices]

        # 应用掩码提取感染区域
        covid_extracted = ct_data * covid_mask

        # 提取新冠区域
        covid_grid = numpy_to_pyvista(covid_extracted, slice_spacing, level)

        plotter.add_mesh(covid_grid.smooth(n_iter=100), color='red', opacity=0.5)


    plotter.export_html(f'Processed_Data/3D_model/3d_model_{nii_file[:-4]}.html')
    print(f'Finish generating {nii_file} 3D model.')


if __name__=="__main__":
    for i in range(1, 9):
        nii_file = f'study_00{i}.nii'
        generate_model_html(nii_file)