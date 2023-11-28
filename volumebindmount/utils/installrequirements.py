import subprocess

def install_requirements(requirements_file):
    try:
        subprocess.check_call(['pip', 'install', '-r', requirements_file])
        print(f"Dependencies installed successfully from {requirements_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")

if __name__ == "__main__":
    requirements_file = "/home/jovyan/work/utils/requirements.txt"  # Replace with the actual path to your requirements.txt
    install_requirements(requirements_file)