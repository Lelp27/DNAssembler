FROM ubuntu:20.04

# apt
RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y git vim wget


# install python3.10

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3.10
RUN apt install python3.10-distutils

# .bashrc
RUN mkdir /home/dev
RUN echo "export LS_COLORS='di=00;36:fi=00;37'" >> ~/.bashrc
RUN echo "cd /home/dev"
