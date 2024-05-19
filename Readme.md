## 肺部可视化大作业

### 概述

此项目旨在通过数据可视化技术实现对肺部结构的可视化，并提供相应的交互界面。以下是项目的技术选型和实现细节。

### 技术选型

- **nii数据处理**：
  - nii数据读取：使用nibabel库
  - nii数据3D可视化：利用PyVista库

- **前后端实现**：
  - 前端：采用React框架
  - 后端：采用Express.js


### 启动React前端：

1. 打开一个命令行终端。
2. 进入到React前端项目的根目录，通常是你创建的项目目录中的`frontend`文件夹。
3. 在命令行中输入以下命令来启动React应用：
   ```
   npm start
   ```
4. 按下回车键，React应用将会开始构建并在默认浏览器中打开。

### 启动Express后端：

1. 打开另一个命令行终端。
2. 进入到Express后端项目的根目录，通常是你创建的项目目录中的`server`文件夹。
3. 在命令行中输入以下命令来启动Express服务器：
   ```
   node app.js
   ```
   或者，如果你的项目使用了`nodemon`等工具来自动重启服务器，你也可以使用：
   ```
   nodemon app.js
   ```
   这样在你每次修改服务器代码后，服务器将会自动重启。

启动后，React前端应用将会在默认端口（通常是`http://localhost:3000`）上运行，并且你的Express后端应用将会在你在代码中指定的端口上运行（通常是`http://localhost:8000`）。你可以通过访问这些地址来查看你的应用程序。记得确保React前端应用能够正确地发送请求到Express后端。

### 实现细节

#### 分割肺部区域

1. **数据预处理**：
   - 读取nii数据，对单层进行K-Means聚类。
   
2. **肺部区域提取**：
   - 使用图形学方法进行两次腐蚀后膨胀操作，得到肺部区域Mask。
   
3. **纯肺部图像生成**：
   - 将Mask和原图像进行AND操作，获取纯肺部图像。
   
4. **批量处理**：
   - 对全部layer实施以上操作，将数据重新保存到processed_study_00x.nii中。

相关文件：
- make_mask.ipynb
- make_masked_nii.py
- make_fat_mask_nii.py
- make_fat_mask.ipynb

#### 3D显示

1. **数据处理**：
   - 使用nii读取数据，进行阈值分割、连通区域分析，提取有用数据。
   
2. **数据转换**：
   - 将读取的3D numpy数组转化为pyvista的UnstructuredGrid对象，并添加层间距离。
   
3. **可视化**：
   - 使用pv.Plotter进行展示。

相关文件：
- 3D_plotmap.py
- 3D_plotmap_smooth.py

#### 可视化以及交互

1. **前后端交互**：
   - 使用React构建前端交互界面，利用Express.js负责后端响应以及调用python文件，获取Model的html和CT图像。

相关文件：
- generate_model_html.py
- ...（其他相关文件）

### 文件详解

- **2D_layer.ipynb**：
  - 用于2D显示，测试原数据并简单实验算法。
  
- **Trash文件夹**：
  - 包含废弃的文件，如废弃的算法和其他功能实现方法。