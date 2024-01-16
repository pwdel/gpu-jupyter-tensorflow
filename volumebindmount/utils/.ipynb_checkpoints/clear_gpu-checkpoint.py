import torch

def clear_gpu_memory():
    """
    Clears unused memory from GPU.
    """
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("torch.cuda.empty_cache() executed.")
    else:
        print("CUDA is not available. GPU memory cannot be cleared.")