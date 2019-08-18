# About
This project allows a photographer to back up their memory cards to another storage medium using a Raspberry Pi, and a USB hub. This is a very travel friendly option to guard against data loss in the case of a failed SD Card or a stolen camera. It's quite inexpensive, compact & lightweight compared to the few highly-specialized devices that do the same thing.

![The backupX system is about the size of a pack of cards](https://github.com/mikeyroy/backupX/blob/gh-pages/DSC06504.jpg)

The copy process uses rsync, and will only copy new files since the last backup. When the copy process is finished, the unit will shutdown. The script will read the label of the source storage and create a folder with the label as the name on the backup drive, so if you are backing up from multiple sources to a single backup the files will go into their respective folders so long as the drive labels of your source drives are unique. If you are backing up from multiple sources, just power cycle the Pi to start a new copy session.

An LED + a resistor can be added to the GPIO pin 13 and a ground pin for a visual indication of activity; solid: waiting for USB devices, flashing: copying. To simplify adding it to the board and minimize space, an [Adafruit LED sequin](https://amzn.to/2RGKzjR) combines both into a single chip. Without the addition of this LED, you have to go off of the Pi's power LED to know when the backup has completed, and the Pi has shut off.

This project has been tested with [Raspberry Pi 4](https://amzn.to/31JsHp9) and the [Raspberry Pi Zero+](https://amzn.to/2FL7yTT) and [Raspbian with Desktop & Recommended Software](https://www.raspberrypi.org/downloads/raspbian/). The [Vilros Raspberry Pi Zero W Kit](https://amzn.to/2FL7yTT) comes with everything you need including the hub. My preferred backup target is a [256 GB USB stick](https://amzn.to/2U8yqkL) and a USB SD card reader with the SD card from the camera is the source.

# Pi 4 vs Pi Zero W
## Speed
In tests of various SD cards and transferring 100GB of image files, the Pi 4 achieved average backup speeds of 1GB/minute while the Pi Zero W is 2.5x slower (~4 hours per 100GB).
## Power Requirements
The Pi 4 requires a dedicated power supply, or a battery that can supply 15W/3A through a USB-C connection. The Pi Zero W can be powered from pretty much anything with a micro-USB cable.
## Size & Weight
The Pi 4 is bigger & heavier, especially when it is in a case, and the Pi 4 has an additional power adapter increasing size & weight even more but while the Pi Zero W is more compact, it requires a USB dongle for the backup targets to it.
## Overall
The Pi 4 is much faster in processing capability and data transfer speeds and feels like a real, usable computing option, while if you were to use the Pi Zero W for any computing, even just web browsing, it is painfully slow. If you need the faster transfer speeds, and want to use the Pi 4 as an ultra-portable computer, or don't mind a bulkier backup option, by all means get that. If you are looking to minimize size and weight in a backup solution, and can manage with the slower transfer speeds, the Pi Zero W is definitely the way to go.

![Raspberry Pi 4 is in the top half with its power adapter, Raspberry Pi Zero W is in the lower half with its USB dongle.](https://github.com/mikeyroy/backupX/blob/gh-pages/backupx-comparing-raspberry-pi-4-to-the-raspberry-pi-zero-w.jpg)
Raspberry Pi 4 is in the top half with its power adapter, Raspberry Pi Zero W is in the lower half with its USB dongle.

# Installation
 - Install Raspbian Full to a new SD Card (Noobs may work, it is untested)
 - Boot the Raspberry Pi and go through the guided setup, the only important thing to set up is wifi 
 - Open Terminal (command line) and enter the following commands:
```
cd ~
git clone https://github.com/mikeyroy/backupX.git
cd backupX
sudo ./enable-service
```
When complete, the Pi will reboot, when it comes back up, go back into the backupX directory and type `sudo ./service-status` to see if the service is running properly. Look for `Active: active (running)` on the 3rd line.

Plug your source and backup drives into the USB hub and verify that the Pi can mount them. If you get an error mounting a specific filesystem, you can likely install a package to mount it. Please raise an issue if you encounter this.

# Usage
 - Your backup medium must have a label of `backupX` (case insensitive) for it to be recognized as the target
 - The backup medium has been tested with Exfat & NTFS (if your preferred drive format doesn't work, file an issue or fork & contribute)
 - Boot the Pi and plug the source and backup storage into the USB hub. The program will wait for both to be plugged in before starting the copy process
 - When the copy process is finished, the Pi will shut down
 - If the backup is interrupted, just power cycle the Pi to continue the copy process

# Testing
 - Using your main computer, place a test file on your source, make sure your backup has a label of `backupX` and is freshly formatted
 - Power up the Pi, with only the USB hub connected, and plug in the source & backup to the USB hub
 - Wait until the Pi powers off
 - On your main computer, verify that the files are on the backup drive 
