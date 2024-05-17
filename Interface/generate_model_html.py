import pyvista as pv

# 创建一个简单的立方体
cube = pv.Cube()

# 创建一个渲染窗口并将立方体添加到场景中
plotter = pv.Plotter()
plotter.add_mesh(cube)

plotter.export_html('3d_model.html')
