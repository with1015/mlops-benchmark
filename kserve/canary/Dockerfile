FROM ubuntu:18.04

WORKDIR /workspace
COPY ./test-send /workspace/

RUN apt-get update
RUN apt install -y python3-dev python3-pip
RUN pip3 install requests

CMD ["sleep", "3600"]
