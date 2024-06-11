import importlib.util
import os
import subprocess

def check_package(package_name):
    package_spec = importlib.util.find_spec(package_name)
    return package_spec is not None

def check_torch_gpu():
    try:
        import torch
        if not torch.cuda.is_available():
            print("Torch is installed but GPU support is not available.")
            print("Please ensure you have the correct CUDA version installed and configured.")
        else:
            print("Torch with GPU support is installed.")
        return True
    except ImportError:
        print("Torch is not installed.")
        return False

def check_environment_variables(variables):
    unset_vars = [var for var in variables if os.getenv(var) is None]
    if unset_vars:
        print(f"The following environment variables are not set: {', '.join(unset_vars)}")
        print("Please set these environment variables accordingly.")
        return False
    else:
        print("All required environment variables are set.")
        return True

def run_nnUNet_predict(input_dict, output_dict, task_id, model):
    command = [
        "nnUNet_predict",
        "-i", input_dict,
        "-o", output_dict,
        "-t", task_id,
        "-m", model
    ]
    try:
        subprocess.run(command, check=True)
        print("nnUNet_predict executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing nnUNet_predict: {e}")

def nnUNet_seg(input_dict, output_dict, task_id, model='2d'):
    torch_installed = check_torch_gpu()
    if not torch_installed:
        print("Please install torch with GPU support from https://pytorch.org/")
        return
    
    nnunet_installed = check_package('nnunet')
    if nnunet_installed:
        print("nnUNet is installed.")
        env_vars = ['nnUNet_raw_data_base', 'nnUNet_preprocessed', 'RESULTS_FOLDER']
        if check_environment_variables(env_vars):
            run_nnUNet_predict(input_dict, output_dict, task_id, model)
    else:
        print("nnUNet is not installed.")
        print("Please install nnUNet using the command: pip install nnUNet")

if __name__ == "__main__":
    nnUNet_seg()
