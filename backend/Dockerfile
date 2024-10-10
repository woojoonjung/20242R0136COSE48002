# =================================
# 최종버전 : canvas:1.1.0 (알파출시되면서 마이너 버전 업그레이드)
# 마지막 반영된 수정 : -
# 이후 추가된 변화(이미지 재생성 필요) : 
# 
# =================================
FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-devel
# =================================
ARG USERNAME=k0seo
ARG UID=1010

RUN echo $USERNAME

RUN useradd -d /home/$USERNAME -m -s /bin/bash -u $UID $USERNAME
RUN echo "${USERNAME}:${USERNAME}" | chpasswd
RUN usermod -aG sudo $USERNAME
# # =================================
RUN apt-get -y update
RUN apt-get -y --allow-unauthenticated upgrade 
RUN apt-get update --fix-missing
RUN apt-get -y install libgl1-mesa-glx 
RUN apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev librsvg2-bin libc6 libvips
RUN apt-get install -y tmux vim htop wget python-setuptools curl git sudo

WORKDIR /home
# =================================
# Custom Setting
# =================================
COPY . .
RUN pip install -r requirements.txt 
RUN pip install --ignore-installed PyYAML 


# =================================
# requirements.txt로 대체할수 있는 방법 찾기
RUN pip install --upgrade pip
RUN pip install psycopg2-binary 
RUN pip install opencv-python
RUN pip install pydantic[email]
RUN pip install keras
RUN pip install tensorflow

WORKDIR /workspace
RUN chmod -R a+w .

USER $USERNAME
ENV HOME /home/$USERNAME