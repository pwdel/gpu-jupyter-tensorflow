import json
from pathlib import Path
from peft import LoraConfig
from transformers import (
    AutoConfig,
    BitsAndBytesConfig,
)
import torch


# Default BitsAndBytes Config
class BitsAndBytesConfig:
    def __init__(self, load_in_4bit, load_in_4bit_use_double_quant, bnb_4bit_quant_type, 
                 bnb_4bit_compute_dtype, quant_method="bitsandbytes",
                 llm_int8_enable_fp32_cpu_offload=False, llm_int8_has_fp16_weight=False, 
                 llm_int8_skip_modules=None, llm_int8_threshold=6.0, load_in_8bit=False):

        self.load_in_4bit = load_in_4bit
        self.load_in_4bit_use_double_quant = load_in_4bit_use_double_quant
        self.bnb_4bit_quant_type = bnb_4bit_quant_type
        self.bnb_4bit_compute_dtype = bnb_4bit_compute_dtype
        self.quant_method = quant_method
        self.llm_int8_enable_fp32_cpu_offload = llm_int8_enable_fp32_cpu_offload
        self.llm_int8_has_fp16_weight = llm_int8_has_fp16_weight
        self.llm_int8_skip_modules = llm_int8_skip_modules
        self.llm_int8_threshold = llm_int8_threshold
        self.load_in_8bit = load_in_8bit


# Overlay Function for BitsAndBytes Config        
def get_bnb_config(config):
    """Gets Bits and Bytes config for quantizing the model."""
    # Mapping string to actual torch data type in a safer way than eval
    dtype_mapping = {
        "torch.bfloat16": torch.bfloat16
    }

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=config['bnb_config']['load_in_4bit'],
        load_in_4bit_use_double_quant=config['bnb_config']['load_4bit_use_double_quant'],
        bnb_4bit_quant_type=config['bnb_config']['bnb_4bit_quant_type'],
        bnb_4bit_compute_dtype=dtype_mapping.get(config['bnb_config']['bnb_4bit_compute_dtype'], torch.bfloat16)
    )
    return bnb_config


# lora configuration
def get_lora_config(config):
    """Gets the Lora Config for creating adapter weights for model."""
    lora_config = LoraConfig(
        r = config['lora_config']['r'],
        lora_alpha = config['lora_config']['lora_alpha'],
        target_modules = config['lora_config']['target_modules'],
        lora_dropout = config['lora_config']['lora_dropout'],
        bias = config['lora_config']['bias'],
        task_type = config['lora_config']['task_type']
    )
    return lora_config


def save_config(config):
    """Writes the config file as json in config folder of model out directory"""
    config_folder_base = config['basic_config']['output_dir'] + 'config/'
    # Create a Path object for the directory
    config_directory = Path(config_folder_base)
    print(f"config directory is: {config_directory}")
    # Check if the config_directory already exists
    if not config_directory.exists():
        # If it doesn't exist, create it
        config_directory.mkdir(parents=True)
    # write out config file
    config_file_path = str(config_directory) + '/config.json'
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)
        print(f"Config file written to {config_file_path}.")