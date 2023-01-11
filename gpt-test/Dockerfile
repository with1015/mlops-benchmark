FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel
MAINTAINER Hyunjoon Jeong <with1015@unist.ac.kr>

WORKDIR /workspace
COPY ./requirements.txt /workspace

RUN pip install -r requirements.txt --use-feature=2020-resolver
EXPOSE 50000
