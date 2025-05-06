#!/usr/bin/bash
export USERNAME=$(whoami)
cd /opt/ventoy/ 
sudo ./VentoyPlugson.sh /dev/sda
