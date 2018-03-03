#!/bin/bash

rank=$1
port=$2

rank=${rank:-prod}
port=${port:-8085}

source ../check_libreosteo.sh
source constant.sh

#MAIN
main() {
    lo_rank_dir=$LO_DIR/$rank
    lo_media_dir=$lo_rank_dir/media
    lo_sql_dir=$lo_rank_dir/sql

    mkdir -p $lo_media_dir $lo_sql_dir
    cat > $lo_rank_dir/docker-compose.yml << EOM
version: '3'

services:
  libreosteo:
    image: $IMAGE
    ports:
      - "$port:8085"
    volumes:
      - ./media:/Libreosteo/media
      - ./sql:/Libreosteo/sql
      - /etc/localtime:/etc/localtime:ro
    restart: always
EOM
    chown -R 1000:1000 $lo_rank_dir
    cd $lo_rank_dir && docker-compose up -d 2> /dev/null
    echo "To use libreosteo: Please launch firefox and go to http://localhost:$port"
}

check_install_all
main