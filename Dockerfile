FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-devel

# =================================
ARG USERNAME=dr_snap
ARG UID=1000

RUN echo $USERNAME

RUN useradd -d /home/$USERNAME -m -s /bin/bash -u $UID $USERNAME
RUN echo "${USERNAME}:${USERNAME}" | chpasswd
RUN usermod -aG sudo $USERNAME
# # =================================
RUN apt-get -y --allow-unauthenticated upgrade
RUN apt-get update --fix-missing
RUN apt-get install -y tmux vim htop wget python-setuptools curl git sudo libssl-dev

WORKDIR /home

USER $USERNAME
ENV HOME /home/$USERNAME


# 4. 모델 코드 클론 및 설치
WORKDIR /workspace
#RUN chmod -R a+w .
# RUN git clone https://github.com/woojoonjung/20242R0136COSE48002.git



# 5. 의존성 설치
RUN pip install --upgrade pip
COPY . .
# RUN pip install -r requirements.txt
