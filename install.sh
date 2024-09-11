#!/bin/bash

echo -e "\033[1;34m <..Installing pingmaster..>  \033[0m"

termux-setup-storage
pkg install -y wget && pkg install -y python
pip install tqdm
pip install ping3

# ลิงก์ GitHub สำหรับดาวน์โหลดไฟล์ pingmaster.py
wget --no-check-certificate 'https://raw.githubusercontent.com/EkromSSH/pingmaster/main/pingmaster.py' -O pingmaster

chmod +x pingmaster
mv pingmaster $PREFIX/bin/pingmaster

echo -e "\033[1;32mScript executed successfully \033[0m"
echo -e "\033[1;33mType pingmaster to run \033[0m"
