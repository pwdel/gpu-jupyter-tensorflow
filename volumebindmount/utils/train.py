

def save_config(self):
    """Writes the config file as json in config folder of model out directory"""
    config_folder = self.CONFIG['basic_config']['output_dir'] + '/config/'
    # Create a Path object for the directory
    directory = Path(config_folder)
    # Check if the directory already exists
    if not directory.exists():
        # If it doesn't exist, create it
        directory.mkdir(parents=True)
    # write out config file
    config_file_path = config_folder + 'config.json'
    with open(config_file_path, 'w') as file:
        json.dump(self.CONFIG, file, indent=4)
        print(f"Config file written to {config_file_path}.")