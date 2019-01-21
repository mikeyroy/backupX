# About
This project allows a photographer to back up their memory cards to another storage medium using a Raspberry Pi, and a USB hub. This is a very travel friendly option to guard against data loss in the case of a failed SD Card or a stolen camera. Since the power requirements are very meager, it can even be powered off of a power bank. It's also quite inexpensive, compact & lightweight compared to the few highly-specialized devices that do the same thing. The only drawback is speed -- 100 GB takes around 4 hours. The intended usage is to run the backup at the end of each day.

The copy process uses rsync, and will only copy new files since the last backup. When the copy process is finished, the unit will shutdown. The script will read the label of the source storage and create a folder with the label as the name, so if you are backing up from multiple sources to a single backup, if the source labels are unique they will go into their respective folders. If you are backing up from multiple sources, just power cycle the Pi to start a new copy session.

An LED + a resistor can be added to the GPIO pin 13 and a ground pin for a visual indication of activity; solid: waiting for USB devices, flashing: copying. To simplify adding it to the board and minimize space, an Adafruit LED sequin combines both into a single chip.

Tested with [Raspberry Pi Zero+](https://amzn.to/2FL7yTT) and [Raspbian with Desktop & Recommended Software](https://www.raspberrypi.org/downloads/raspbian/). The [Vilros Raspberry Pi Kit](https://amzn.to/2FL7yTT) comes with everything you need including the hub. My preferred backup target is a [256 GB USB stick](https://amzn.to/2U8yqkL) and a USB SD card reader with the SD card from the camera is the source.

# Installation
 - Install Raspbian Full to a new SD Card (Noobs may work, it is untested)
 - Boot the Raspberry Pi and go through the guided setup, the only important thing is to set up wifi 
 - Open Terminal (command line) and enter the following commands:
```
cd ~
git clone https://github.com/mikeyroy/backupX.git
cd backupX
sudo ./enable-service
```
When complete, the Pi will reboot, when it comes back up, go back into the backupX directory and type `sudo ./service-status` to see if the service is running properly. Look for `Active: active (running)` on the 3rd line.

# Usage
 - Your backup medium must have a label of `backupX` for it to be recognized as the target.
 - Boot the Pi and plug the source and backup storage into the USB hub. The program will wait for both to be plugged in before starting the copy process
 - When the copy process is finished, the Pi will shut down
 - If the back up is interrupted, power cycle the Pi to continue the copy process
