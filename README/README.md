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
* That being said, torch does not have good support for conda. So the way we have to do this is, once the jupyter notebook is up and running:
1. Open up a terminal. Navigate to the utils/ directory.
2. Run python installrequirements.py
3. You can verify that torch has been installed by going into a notebook and attempting `import torch`.

This should install torch. Unfortunately, it is part of the container and not part of the docker image including the conda installation, so it has to be redone if the container fails.
