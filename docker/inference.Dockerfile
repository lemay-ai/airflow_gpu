FROM tensorflow/tensorflow:2.7.0-gpu


RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt-get install -y tzdata

# Pick up some TF dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        pkg-config \
        python \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \
        software-properties-common \
        unzip \
        nano \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install requirements.txt
COPY requirements.txt /tmp
WORKDIR /tmp
RUN python3 -m pip install -r /tmp/requirements.txt



RUN mkdir -p /inference && chmod a+wrx /inference
RUN mkdir -p /models && chmod a+wrx /models
RUN mkdir -p /data && chmod a+wrx /data
WORKDIR "/inference"


ENV PATH /usr/local/cuda/bin:/usr/local/cuda-11.1/bin:/usr/local/cuda-11.2/bin:/usr/local/cuda-11.3/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:/usr/local/cuda-11.1/lib64:/usr/local/cuda-11.2/lib64:/usr/local/cuda-11.3/lib64



WORKDIR /inference
COPY tmp/main_inference.py /inference/

