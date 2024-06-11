import nibabel as nib
import numpy as np
import scipy.ndimage as ndi
import pyvista as pv
from skimage import measure

    # 将3D numpy数组转换为pyvista的UnstructuredGrid对象，添加层间距离，并增加Marching Cubes的Level
def numpy_to_pyvista(vol, slice_spacing=1.0, level=-300):
    verts, faces, _, _ = measure.marching_cubes(vol, level=level)
    
    # 调整顶点位置，增加层间距离
    verts[:, 2] *= slice_spacing
    
    faces = np.hstack([np.full((faces.shape[0], 1), 3), faces]).astype(np.int64)
    grid = pv.PolyData(verts, faces)
    return grid

def generate_model_html(nii_file):
    print(f'Generating {nii_file} patient 3D model...')
    # 加载原始nii数据
    ct_image = nib.load('Data/'+nii_file)
    ct_data = ct_image.get_fdata()

    # 加载mask nii数据
    mask_image = nib.load('Processed_Data/nii_mask_files/'+nii_file)
    mask_data = mask_image.get_fdata()

    # 新冠感染区域
    covid_mask = np.where(mask_data == 3, mask_data, 0)

    # 肺部区域
    lung_mask = np.zeros_like(mask_data)
    lung_mask[mask_data == 1] = 1
    lung_mask[mask_data == 2] = 1

    # 应用掩码提取肺部
    lung_extracted = ct_data * lung_mask

    # 应用掩码提取感染区域
    covid_extracted = ct_data * covid_mask


    # 设置层间距离，例如每层之间的距离设为10.0，以及Marching Cubes的Level
    slice_spacing = 10.0
    level = -500  # 适当调整level的值

    # 提取肺部区域
    lung_grid = numpy_to_pyvista(lung_extracted, slice_spacing, level)

    # 提取新冠区域
    covid_grid = numpy_to_pyvista(covid_extracted, slice_spacing, level)


    # 创建一个Plotter对象进行3D展示
    plotter = pv.Plotter()
    plotter.add_mesh(lung_grid.smooth(n_iter=100), color='white', opacity=0.5)  # 应用平滑算法
    plotter.add_mesh(covid_grid.smooth(n_iter=100), color='red', opacity=0.5)  # 应用平滑算法

    plotter.export_html(f'Processed_Data/3D_model/3d_model_{nii_file[:-4]}.html')
    print(f'Finish generating {nii_file} 3D model.')


if __name__=="__main__":
    nii_file = 'study_007.nii'
    generate_model_html(nii_file)