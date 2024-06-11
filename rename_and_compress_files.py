import os
import shutil
import gzip

def rename_and_compress_files(source_folder, target_folder):
    # 如果目标文件夹不存在，创建它
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        # 构建完整的文件路径
        source_file = os.path.join(source_folder, filename)
        
        # 确保只处理文件，而不是目录
        if os.path.isfile(source_file):
            # 获取文件名和扩展名
            name, ext = os.path.splitext(filename)
            # 构建新的文件名
            new_filename = f"{name}_0000{ext}"
            # 构建新的文件路径
            new_file = os.path.join(target_folder, new_filename)
            # 复制并重命名文件
            shutil.copy2(source_file, new_file)
            
            # 构建压缩包文件名
            gz_filename = f"{new_filename}.gz"
            gz_file_path = os.path.join(target_folder, gz_filename)
            
            # 打开源文件和目标压缩包文件
            with open(new_file, 'rb') as f_in, gzip.open(gz_file_path, 'wb') as f_out:
                # 将源文件内容写入压缩包文件
                shutil.copyfileobj(f_in, f_out)

            # 删除重命名后的源文件
            os.remove(new_file)
            
            print(f"文件 {new_filename} 已打包为 {gz_filename}")

    print("所有文件已成功重命名并打包为 .gz 压缩包。")


if __name__ == "__main__":
        # 定义源文件夹和目标文件夹
    source_folder = 'Data'  # 替换为你的源文件夹路径
    target_folder = 'dataset_predict'
    rename_and_compress_files(source_folder, target_folder)