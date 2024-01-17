import torch

def show_torch_and_gpu_stats():
    print(torch.__version__)
    if torch.cuda.is_available():
        print("GPU is available.")
    else:
        print("GPU is not available. Check your CUDA installation.")

    current_device = torch.cuda.current_device()
    print(f"Current GPU device: {current_device}")

    device_properties = torch.cuda.get_device_properties(0)  # Replace 0 with the desired GPU index
    print(f"GPU Name: {device_properties.name}")
    print(f"GPU Memory Capacity: {device_properties.total_memory / 1e9} GB")
