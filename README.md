# sendot
Interaction with Sendot FluoMini Pro


## Sendot FluoMini Pro

Sendot FluoMini Pro is portable device what is calculating photosynthesis efficiency. You can find more information via (https://sendot.nl/en/sensoren/fotosynthese/).

In my case I am using this sensor, connected to Aranet 4-20mA sensor (https://aranet.com/product/aranet-4-20ma-transmitter/) so all data are logged to Aranet PRO station and later processed via other scripts.
For new project, thanks to Arie Draaijer, I was able to write simple script to collect not only photosynthesis efficiency, but also Fmax value for later NPQ value calculation.

#### Equippment used

It will come in handy to have:
* Raspberry Pi 4 4Gb RAM
* SD card or preferrably USB-drive - 8gb or more
* Protective case with ventilator and heat sink

#### Preparing Raspberry Pi

In my case I used Raspberry Pi OS with desktop, with all usual updates. 
First what I did - changed user from original `pi` to something more meaningful, as well as changed ssh port and multiple other bits and pieces - this is another topic.

For this project you need to install pyserial, not to be mistaken with serial:

`pip3 install pyserial`

Connect you sensor to USB port.

That must do the trick - if you are able to detect your device with

`lsusb`

what should return something similar to:
```
sendot@sendot:~ $ lsusb
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 004: ID 0403:6015 Future Technology Devices International, Ltd Bridge(I2C/SPI/UART/FIFO)
Bus 001 Device 003: ID 0403:6015 Future Technology Devices International, Ltd Bridge(I2C/SPI/UART/FIFO)
Bus 001 Device 002: ID 2109:3431 VIA Labs, Inc. Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

then you can carry on with detecting your port, what in most cases will be `/dev/ttyUSB0` or similar.

Command to check port - `dmesg | grep 'ttyUSB'` 

Should return you:
```
sendot@sendot:~ $ dmesg | grep 'ttyUSB'
[    5.904020] usb 1-1.1: FTDI USB Serial Device converter now attached to ttyUSB0
[    5.934061] usb 1-1.2: FTDI USB Serial Device converter now attached to ttyUSB1
```
Where in my case I have two devices connected to one RPi. Mark down port, and use it in the file `sendot_serial_log.py` - replace `port='dev/ttyUSB1'` with one you have.

As Sendot uses FTDI serial to USB chip, you can check whether device ir recognised:
```
sendot@sendot:~ $ dmesg | grep FTDI
[    2.532278] usb 1-1.1: Manufacturer: FTDI
[    2.811778] usb 1-1.2: Manufacturer: FTDI
[    5.767450] usbserial: USB Serial support registered for FTDI USB Serial Device
[    5.767672] ftdi_sio 1-1.1:1.0: FTDI USB Serial Device converter detected
[    5.904020] usb 1-1.1: FTDI USB Serial Device converter now attached to ttyUSB0
[    5.904404] ftdi_sio 1-1.2:1.0: FTDI USB Serial Device converter detected
[    5.934061] usb 1-1.2: FTDI USB Serial Device converter now attached to ttyUSB1
```

After this step you are ready to continue to script. If you run in to the problems, it might be because of permissions of usb port,  I am not sure what is the right way to set this up, but I changed permissions in `sudo nano /lib/udev/rules.d/50-udev-default.rules` . Prefferably try to ommit this step, as I am not fully aware what problems it can cause in future.

To get you going, last things you need to do:
* create `.txt` file with desired name, open it, and put this as first two rows:
```
time; eff; umol; fmin; fmax

```
* in file `sendot_serial_log.py` in 8th line change existing link with link to your file. 

This script will allow you with simple `python3 sendot_serial_log.py` to make measurement and to save it to file.

Im my case, this scrip is called from another scrip depending to light conditions - every minutes I check for presence of light, and if light is present, I call log script, and then next measurement is doen after 5 cycles of photoperiod detecting, while during the night I perform measurement every hour.

#### Checking connection with miniterm.py

If you still is not sure whether connection is working or not, you can check it with following command, just be sure that you change to port what you have:

`python3 -m serial.tools.miniterm /dev/ttyUSB0 19200`

This should open a miniterm, where after each automated measurement timed by Sendot device you should see the output of measurements. To quit miniterm, simply type `Ctrl+]` and you are out. 

#### Last remarks

This script is available as is without any liability, and user of this script should fully understand that this script is written by person with minimal knowledge in programming.

It was not easy to get this going, as this was first time when I had a need to write something for serial communication, but for me this script works out pretty well, despite the fact that I am not fully aware what is going on under the hood.
