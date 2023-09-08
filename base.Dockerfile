# base.Dockerfile
ARG NVIDIA_CUDA_BASE

# Use the NVIDIA CUDA base image as the starting point
FROM $NVIDIA_CUDA_BASE

# Set environment variables (if needed)
#ENV MY_ENV_VAR=my_value

# Install necessary packages
#RUN apt-get update && apt-get install -y \
#    package1 \
#    package2 \
    # Add more packages as needed

# Copy files and configurations
# COPY my_files /path/in/container

# Set any other configurations, create directories, etc.

# Set the working directory
WORKDIR /home

# Define the command to run when a container is started from this image
CMD ["/bin/bash"]
