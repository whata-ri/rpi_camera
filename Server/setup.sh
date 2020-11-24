#/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)

cd $SCRIPT_DIR/docker

# create docker image
docker build -t particle_count:latest .

cd -
# create docker container
docker run --gpus all --name particle_count -itd particle_count:latest -v $SCRIPT_DIR:/workspace
