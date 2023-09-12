# Reference Documentation

* [Docker GPU Support](https://docs.docker.com/compose/gpu-support/)

# Notes On Getting This Running

1. Install fresh Ubuntu 22 LTS on a machine with an Nvidia GPU.
2. Install prerequisites in our linux setup file.
3. Test to ensure that `nvidia-smi` command works within docker container.

# How to Use This Repo

* constants.env is a file that contains various constants across the below files to keep things consistent.
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

## Verifying SMI in the Notebook

* Open a terminal and enter "nvidia-smi" which will show the gpu you have access to.

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
