clear -x
echo Running Mainserver Docker...

# Allocate Physical Devices for Docker
if [ -z "$1" ]
then
    echo GPU \# not allocated
    exit 1
else
    if [ $1 = "all" ]
    then
        devices=all
    else
        devices=\"device=$1\"
    fi
fi

if [ -z "$2" ]
then
        name=''
else
        name=$2
fi

# Allocate shared memory
memsize=32G

# Docker run
docker run \
        -p 3612:3612 \
        -u k0seo \
        --shm-size $memsize \
        --gpus $devices \
    -v /home/k0seo0330/capston/backend:/workspace \
        --name $name \
        --hostname k0seo \
        -ti k0seo/cap:1.0 \
/bin/bash