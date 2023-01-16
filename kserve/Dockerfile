FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel

WORKDIR /workspace
COPY ./requirements.txt /workspace
RUN pip install --no-cache-dir -r ./requirements.txt --use-feature=2020-resolver

