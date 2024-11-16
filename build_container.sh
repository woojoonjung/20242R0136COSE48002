
clear -x
echo Setting Mainserver Docker...

IMAGE_NAME="drsnap"

if [ -z "$1" ]
then
        name=''
else
        name=$1
fi

# Allocate shared memory
memsize=32G

# Docker run
docker run \
        -p 1105:1105 \
        -u root \
        --shm-size $memsize \
        --gpus all \
    -v drsnap:/drsnap \
        --name $name \
        -ti drsnap:ver1

echo Running Mainserver Docker...

/bin/bash