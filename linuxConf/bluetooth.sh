# Script to install Realtek RTL8761B bluettooth dongle dependencies on Ubuntu 20.04
# Doc: https://linuxreviews.org/Realtek_RTL8761B
# Requires sudo access
# fantoni[o|0] (25/04/2021)

# Install bluetooth firmware
mkdir -p .tmp
cd .tmp || { echo "Can't access .tmp directory"; exit 1; }

## Download files
wget --no-check-certificate https://raw.githubusercontent.com/Realtek-OpenSource/android_hardware_realtek/rtk1395/bt/rtkbt/Firmware/BT/rtl8761b_config
wget --no-check-certificate https://raw.githubusercontent.com/Realtek-OpenSource/android_hardware_realtek/rtk1395/bt/rtkbt/Firmware/BT/rtl8761b_fw

## Rename and move files
sudo mv rtl8761b_fw /usr/lib/firmware/rtl_bt/rtl8761b_fw.bin
sudo mv rtl8761b_config  /usr/lib/firmware/rtl_bt/rtl8761b_config.bin
cd ..
rm -rf .tmp/

# Pair device. The configuration is for Bose QC35 II, but I think it will work for many other devices
# Doc: https://askubuntu.com/questions/833322/pair-bose-quietcomfort-35-with-ubuntu-over-bluetooth

## First clean the state: remove devices from paired list in Ubuntu
## Hold bluetooth switch for 10 seconds in the headphones to remove paired devices

## Edit and change bluetooth configuration. Deactivate low energy bluetooth for pairing
sudo sed -i 's/#ControllerMode = dual/ControllerMode = bredr/' /etc/bluetooth/main.conf

## Restart bluetooth
sudo systemctl restart bluetooth.service

## Optionally re-activate low energy bluetooth after pairing the device
#sudo sed -i 's/ControllerMode = bredr/\#ControllerMode = dual/' /etc/bluetooth/main.conf
#sudo systemctl restart bluetooth.service
