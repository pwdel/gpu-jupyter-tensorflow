# jupyter.Dockerfile

# args - Define the base image name, fed in as a build arugment
ARG LOCAL_BASE_IMAGE_NAME

# use the locally built base image as a starting point
FROM $LOCAL_BASE_IMAGE_NAME

# common environemnt variables
ENV NB_USER jovyan
ENV NB_UID 1000
ENV NB_PREFIX /
ENV HOME /home/$NB_USER
ENV SHELL /bin/bash

# args - software versions
ARG S6_ARCH="amd64"
 # renovate: datasource=github-tags depName=just-containers/s6-overlay versioning=loose
ARG S6_VERSION=v2.2.0.3

# set shell to bash
SHELL ["/bin/bash", "-c"]

# install - usefull linux packages
RUN export DEBIAN_FRONTEND=noninteractive \
   && apt-get -yq update \
   && apt-get -yq install --no-install-recommends \
   apt-transport-https \
   bash \
   bzip2 \
   ca-certificates \
   curl \
   git \
   gnupg \
   gnupg2 \
   locales \
   lsb-release \
   nano \
   software-properties-common \
   tzdata \
   unzip \
   vim \
   wget \
   zip \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*

# install - s6 overlay
RUN export GNUPGHOME=/tmp/ \
   && curl -sL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}-installer" -o /tmp/s6-overlay-${S6_VERSION}-installer \
   && curl -sL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}-installer.sig" -o /tmp/s6-overlay-${S6_VERSION}-installer.sig \
   && gpg --keyserver keys.gnupg.net --keyserver pgp.surfnet.nl --recv-keys 6101B2783B2FD161 \
   && gpg -q --verify /tmp/s6-overlay-${S6_VERSION}-installer.sig /tmp/s6-overlay-${S6_VERSION}-installer \
   && chmod +x /tmp/s6-overlay-${S6_VERSION}-installer \
   && /tmp/s6-overlay-${S6_VERSION}-installer / \
   && rm /tmp/s6-overlay-${S6_VERSION}-installer.sig /tmp/s6-overlay-${S6_VERSION}-installer

# create user and set required ownership
RUN useradd -M -s /bin/bash -N -u ${NB_UID} ${NB_USER} \
   && mkdir -p ${HOME} \
   && chown -R ${NB_USER}:users ${HOME} \
   && chown -R ${NB_USER}:users /usr/local/bin \
   && chown -R ${NB_USER}:users /etc/s6

# set locale configs
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
   && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# switch to user root for Miniforge and Conda Installs
USER root

# args - software versions
ARG MINIFORGE_ARCH="x86_64"
# renovate: datasource=github-tags depName=conda-forge/miniforge versioning=loose
ARG MINIFORGE_VERSION=4.10.1-4
ARG PIP_VERSION=21.1.2
ARG PYTHON_VERSION=3.9.0

# setup environment for conda
ENV CONDA_DIR /opt/conda
ENV PATH "${CONDA_DIR}/bin:${PATH}"
RUN mkdir -p ${CONDA_DIR} \
   && echo ". /opt/conda/etc/profile.d/conda.sh" >> ${HOME}/.bashrc \
   && echo ". /opt/conda/etc/profile.d/conda.sh" >> /etc/profile \
   && echo "conda activate base" >> ${HOME}/.bashrc \
   && echo "conda activate base" >> /etc/profile \
   && chown -R ${NB_USER}:users ${CONDA_DIR} \
   && chown -R ${NB_USER}:users ${HOME}

# switch to NB_UID for installs
USER ${NB_UID}

# install - conda, pip, python
RUN curl -sL "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-${MINIFORGE_ARCH}.sh" -o /tmp/Miniforge3.sh \
   && curl -sL "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-${MINIFORGE_ARCH}.sh.sha256" -o /tmp/Miniforge3.sh.sha256 \
   && echo "$(cat /tmp/Miniforge3.sh.sha256 | awk '{ print $1; }') /tmp/Miniforge3.sh" | sha256sum --check \
   && rm /tmp/Miniforge3.sh.sha256 \
   && /bin/bash /tmp/Miniforge3.sh -b -f -p ${CONDA_DIR} \
   && rm /tmp/Miniforge3.sh \
   && conda config --system --set auto_update_conda false \
   && conda config --system --set show_channel_urls true \
   && echo "conda ${MINIFORGE_VERSION:0:-2}" >> ${CONDA_DIR}/conda-meta/pinned \
   && echo "python ${PYTHON_VERSION}" >> ${CONDA_DIR}/conda-meta/pinned \
   && conda install -y -q \
      python=${PYTHON_VERSION} \
      conda=${MINIFORGE_VERSION:0:-2} \
      pip=${PIP_VERSION} \
   && conda update -y -q --all \
   && conda clean -a -f -y \
   && chown -R ${NB_USER}:users ${CONDA_DIR} \
   && chown -R ${NB_USER}:users ${HOME}

# Activate Conda Environment to install requirements
RUN conda create -y -n tf_gpu_env python=3.9.0

# Now go into that Conda environment as a shell
SHELL ["conda", "run", "-n", "tf_gpu_env", "/bin/bash", "-c"]

# The following will take a long time to build.

# Install dependencies using the environment.yaml files
# tf_gpu_env.yaml first
COPY --chown=jovyan:users tf_gpu_env.yaml /tmp/tf_gpu_env.yaml
RUN conda env update -n tf_gpu_env -f /tmp/tf_gpu_env.yaml \
   && rm /tmp/tf_gpu_env.yaml \
   && jupyter lab --generate-config \
   && rm -rf ${HOME}/.cache/yarn \
   && chown -R ${NB_USER}:users ${CONDA_DIR} \
   && chown -R ${NB_USER}:users ${HOME}

# Register the conda environment as a Jupyter kernel
RUN python -m ipykernel install --user --name=tf_gpu_env

# Activate Conda Environment to install requirements
RUN conda create -y -n pt_gpu_env python=3.9.0

# Now go into that Conda environment as a shell
SHELL ["conda", "run", "-n", "pt_gpu_env", "/bin/bash", "-c"]

# then pt_gpu_env.yaml
COPY --chown=jovyan:users pt_gpu_env.yaml /tmp/pt_gpu_env.yaml
RUN conda env update -n pt_gpu_env -f /tmp/pt_gpu_env.yaml \
   && rm /tmp/pt_gpu_env.yaml \
   && jupyter lab --generate-config \
   && rm -rf ${HOME}/.cache/yarn \
   && chown -R ${NB_USER}:users ${CONDA_DIR} \
   && chown -R ${NB_USER}:users ${HOME}

RUN python -m ipykernel install --user --name=pt_gpu_env

# s6 - copy scripts
COPY --chown=jovyan:users s6/ /etc

# switch to user root to create directory
USER root

# s6 - 01-copy-tmp-home
RUN mkdir -p /tmp_home \
   && cp -r ${HOME} /tmp_home \
   && chown -R ${NB_USER}:users /tmp_home

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID

EXPOSE 8888

ENV NB_PREFIX /

# Noop Change
RUN echo "anoner anoner noop change."

# Copy Entrypoint Script into Image
COPY entrypoint /usr/local/bin/
COPY conda_jupyterlaunch /usr/local/bin

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "-n", "tf_gpu_env", "bash", "/usr/local/bin/entrypoint"]
