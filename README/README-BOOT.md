# Reference Documentation

* [Docker GPU Support](https://docs.docker.com/compose/gpu-support/)

# Notes On Getting This Running

1. Install fresh Ubuntu 22 LTS on a machine with an Nvidia GPU.
2. Install prerequisites in our linux setup file.
3. Test to ensure that `nvidia-smi` command works within docker container.

# How to Use This Repo

* .env is a file that contains various constants across the below files to keep things consistent.
* base.Dockerfile builds a cuda ubuntu 22 image which can connect to the underlying nvidia gpu. 
* jupyter.Dockerfile uses the cuda ubuntu 22 as a base, and then builds jupyter on top of that.
* buildimageandtag is a bash script which ties the two together and tags it so that docker-compose can use it.
* docker-compose.yaml has two services, a test and cudajuypyter service.

## Two Main Commands

* ./testexposedgpus ... runs the test service, which just tests to ensure that the gpu and nvidia smi can be reached. If you run ./testexposedgpus this will verify with an smi printout.
* ./runjupytergpu ... will take the previously tied together base.Dockerfile and jupyter.Dockerfile and runs it with gpu connected.

## Finding the Notebook

After running ./runjupytergpu, you might not see any success messages. If not you can check out the docker logs to find where to visit the notebook with:

```
docker compose logs
```

However generally, you should find the notebook in your browser at either {localhost}:8888/lab or if you are connecting to this remotely, at {host machine ip}:8888/lab

## Verifying SMI in the Notebook

* Open a terminal and enter "nvidia-smi" which will show the gpu you have access to.

* The file TEST_GPU.ipynb has lots of various tests which can be used to verify various operations.

## Installing Tensorflow GPU

* Need a compatible version of tensorflow-gpu

```
pip install tensorflow-gpu==2.11.0
```

## Verifying GPU Access in Tensorflow

```
tf.config.list_physical_devices(
    device_type=None
)
```
## Anaconda Requirements

* Due to how this is set up and for ease of customization, the requirements file is within the conda dependency setup, environment.yaml.
* The general format is:

```
cat environment.yaml
name: tf_gpu_env
channels:
  - anaconda
  - conda-forge
dependencies:
  - anaconda::tensorflow-gpu=2.4.1
  - conda-forge::jupyterlab=2.0.0 # 28 Feb 2020, last known date of working with GeForce 1070
  - numpy=1.23.0
  - pandas=1.5.2
  - ipykernel
```

* To set up new dependencies, you have to enter them in this environment.yaml file within the format shown above and then re-build the image with ./buildimageandtag .

## Torch and Non-Anaconda Requirements

* Python package management is done through either pip or conda. Conda is the package management system tied to Jupyter notebook environments.
* That being said, torch does not have good support for conda. So the way we have to do this is, once the container and jupyter notebook is up and running:

### Torch Within the Container

* To install Torch within the container but not necessarily a Lab kernel (there is a difference):

1. Open up a terminal. Navigate to the utils/ directory.

2. Run:
 
```
python installrequirements.py
```

3. You can verify that torch has been installed by going into a notebook and attempting `import torch`.

* This should install torch. Unfortunately, it is part of the container and not part of the docker image including the conda installation, so it has to be redone if the container fails.
* Also, please note that this does not install torch in any given Jupyter Lab kernel, which...each have their own kernel on top of the Jupyterlab Terminal, which seems to be more something that's just running in the Docker container.

### Torch Within a Notebook

* To be able to install Torch within a notebook, you have to open up a notebook and run:

```
!pip install -U torch
```
* the -U stands for upgrade.
* The last known working version was 2.1.1+cu121
* That being said, once you do that, you might have some unexpected effects and things still might not work properly.
* So, you may need to hit, "restart kernel," in order to get the correct version of torch working. To do this you go to Kernel >> Restart Kernel in the menu.
* To verify, do:

```
import torch
print(torch.__version__)
```
* Which should show 2.1.2+cu121 as the version.
* Moreover:

```
!pip list | grep torch
```

* Should show torch 2.1.2 as the version.
* Using the following commands:

```
import torch
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
```

* You should get the following to verify that the GPU is available.

```
2.1.1+cu121
GPU is available.
Current GPU device: 0
GPU Name: NVIDIA GeForce GTX 1070
GPU Memory Capacity: 8.501919744 GB
```
