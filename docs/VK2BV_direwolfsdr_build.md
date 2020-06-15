VK2BV Direwolf - Build SDR Lite Image



# Build the SDR Lite Image

This document covers the SDR lite image. The lite image does not include the desktop components and is meant to be run via ssh access, network and or boot files.

There is also a [full image build](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolffull_build.md). This starts with the full desktop version. This opens a whole can of worms in its own right.

From time to time you may need to completely rebuild the image. These instructions and some scripts represent a minimal set of installs and script changes that were needed to build the image. I ended up automating several of these steps and these notes are the result. Your mileage may vary!!!

# Parts for the SDR lite image

  - Tested with Raspberry Pi B+ to Raspberry Pi 4 (also now tested A+ and zero)
  - 8Gb+ SD card
  - RTL-SDR type sdr dongle.
  - 5V power for the Pi (initially it can be built from your PC USB, but later you will need around 1A [5W])
  - Optional
    - GPS - this is not included in the setup scripts yet
    - RTC

For the Lite image I recommend an 16Gb SD card (I used to recommend 4/8Gb but they are hard to come by)
If you have an older Pi, I recommend at least a Pi B+ (the start of the micro SD ports and 4 x USB). However if you have a pi B that should work for the SDR or lite build.

If you are buying new then get a Pi 3B+ or PiZeroW, as they have more than enough cpu for this.

Source for lite image:

choose the raspbian Lite image.

https://www.raspberrypi.org/downloads/raspbian/

There are several articles on how to create an image on the SD using these files. I don't recommend using NOOBS for this project. (If you have that in your kit set aside for now)

ssh software - it's builtin on most Mac and Linux. For windows
  - MobaXterm (this seems very good and the free limitations should not be a problem)
  - Bitvise SSH Client
  - More here in future


For the install I am assuming you are using an ethernet connection and have reasonable internet access.

For wifi only devices I have included a sample text file you can use during boot.

### Latest Raspberry Jessie image does not enable ssh by default.

To fix, after you have created the image load the sd card up on the pc again and you should get a disk volume called "boot".
Open this drive in explorer/finder and create a file called ```ssh``` in the directory. In windows you can right click and create a text file saving as ssh (without the `.txt`)

* for wifi devices create a text file with your wifi SSID information

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=AU
network={
    ssid="MYSSID"
    psk="thepassword"
}
```

save the files to the same "boot" directory above. The file must be called  `wpa_supplicant.conf` again make sure it doesn't have a `.txt` extension

* If you ever need to change to a new wifi then you can repeat this process, the raspi checks for this file during the boot and copies the details over.


To start the process you just need the Pi plugged in.

login is: pi/raspberry

boots to the shell  (ssh available)

basic config stuff:


### Initial Setup

```
sudo raspi-config
```

The Raspi-config is a curses based menu,  uses arrow, tab and enter keys, space bar to de/select options. The following options are what I would suggest changing.



    -   expand filesystem [not needed since 2018]
    -   Internationalization/Change locale : en_AU.UTF-8 and remove en_GB entry
    -     Select en_AU.UTF-8 as default
    -   Internationalization/Change timezone : Australia/Sydney
    -   advanced/hostname   : vkxxxpi
    -   reboot

After the reboot log in and we will first update the system software.

```shell
sudo apt-get update
sudo apt-get -y upgrade
sudo reboot
```

Now we start with some installs, from here I am using apt-get -y to avoid the confirmation prompt

### Support for git and nslookup

full_build users can follow these steps in a console(x-terminal)

```shell
sudo apt-get -y install libasound2-dev cmake build-essential git-core
sudo apt-get -y install dnsutils gawk automake libtool
sudo apt-get -y install libudev-dev python-dev swig libusb-1.0-0-dev texinfo
```


### gpsd install
This next section is to support gps attached to the Pi, even if you don't have the gps you can install this now and it will build in the right bits for later.

```
sudo apt-get -y install gpsd libgps-dev gpsd-clients python-gps
```

#### optional git settings - not sure if these are needed
These entries may not be needed for most interactions with git so dont enter yet (unless git prompts you for the information)<br>
  - git config --global user.name “vkxxx"<br>
  - git config --global user.email xxx@xxx.com<br>

### Clone these documents and script files for rtl-sdr

```shell
cd ~
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr
mkdir build
cd build
cmake .. -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
make
sudo make install
```




### Now we get direwolf



```shell
cd ~
git clone https://www.github.com/wb2osz/direwolf
cd direwolf
mkdir build
cd build
cmake ..
make
sudo make install
make install-conf
cd ~
```

So now direwolf is installed but not yet configured.

At this stage I recommend a reboot and plugging in the sdr dongle.

## Configure direwolf

By default direwolf creates a file  direwolf.conf  in the home directory, this contains the information you need to create most configs. I have included a script that will gather some details and create a new file called direwolf.sample.

first of all keep a copy of the default direwolfconfig

```shell
cd ~
mv direwolf.conf direwolf.origconf
```

I have included a script in the steps below that will gather some details and create a new series of files for different usage.

To test the basic functions at this point.
use lsusb to see if the SDR is mounted and rtl_test to see if rtl can read from the dongle. Then use Ctrl-C to cancel the test.

```shell
pi@bvdirew:~ $ lsusb
Bus 001 Device 005: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T
Bus 001 Device 004: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. SMSC9512/9514 Fast Ethernet Adapter
Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. SMC9514 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
pi@bvdirew:~ $ rtl_test
Found 1 device(s):
  0:  Realtek, RTL2838UHIDIR, SN: 00000001

Using device 0: Generic RTL2832U OEM
Detached kernel driver
Found Rafael Micro R820T tuner
Supported gain values (29): 0.0 0.9 1.4 2.7 3.7 7.7 8.7 12.5 14.4 15.7 16.6 19.7 20.7 22.9 25.4 28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0 49.6
[R82XX] PLL not locked!
Sampling at 2048000 S/s.

Info: This tool will continuously read from the device, and report if
samples get lost. If you observe no further output, everything is fine.

Reading samples in async mode...
^CSignal caught, exiting!

User cancel, exiting...
Samples per million lost (minimum): 0
Reattached kernel driver
```

## Testing direwolf

```
cd ~
direwolf -t 0
```

This should read /home/pi/direwolf.conf and start up (-t 0 turns off the colour outputs). It will probably show errors if no configuration, thats ok we just want to see that it's installed.


## Configuring direwolf as a service

Scripts to support configuration, testing and startup are included in the git package VK2BV_Direwolf

Documentation about the scripts and the order of use is here [VK2BV direwolf scripts](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolf_scripts.md) document section

You can use the diremenu commands to enable and disable the service.

* Note that the sdr startup is different to normal direwolf, either use the the `direswitch` menu option or manually edit the /etc/init.d/direwolf file with:

```
DAEMON=/usr/local/bin/direwolf
or
DAEMON=/usr/local/bin/direwsdr
```
near the top of the file.

* to enable the service:

> ...
> h) sudo service direwolf status
> i) sudo systemctl enable direwolf.service
> j) sudo systemctl disable direwolf.service
> q) quit this menu
>
> Enter option :h
> ● direwolf.service - direwolf - A TNC and aprs
>    Loaded: loaded (/lib/systemd/system/direwolf.service; disabled)

The service is currently disabled from automatic startup

>    Active: inactive (dead)

The service is not running

>
> Jan 27 15:20:45 vk2psfpi sudo[1899]: pam_unix(sudo:session): se....



Use menu option i) sudo systemctl enable direwolf.service
to enable startup after reboots




## Extra Pieces

### Fixed IP Address on the new raspbian since jessie

The fixed ip address information is now located in `/etc/dhcpcd.conf`

This creates a static entry 192.168.5.50



> interface eth0
> static ip_address=192.168.5.50/24
> static routers=192.168.5.1
>\# static domain_name_servers=8.8.8.8

### Command line wifi

THIS SECTION IS EXPERIMENTAL NOT EXTENSIVELY TESTED


Finding SSID's

```shell
sudo iwlist wlan0 scan | grep -e Cell -e ESSID -e 'IE: IEEE'
```

Edit the file

```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Create an entry

> network={
>     ssid="The_ESSID_from_earlier"
>     psk="Your_wifi_password"
> }
>
> network={
>     ssid="anotherSSID"
>     psk="Thepassphrase"
> }


Note: creating a secure entry
You can use the wpa_passphrase command to create an encrypted version of the password

```
wpa_passphrase anotherSSID Thepassphrase
```
Generates
> network={
> 	ssid="anotherSSID"
> 	#psk="Thepassphrase"
> 	psk=8ecbe91f1a0eea741cdc1f8415383c732cddc9701a0262b26198d3f87d80a10e
> }

which can be used in the supplicant file (without the text based password line!)




### Other

The avahi/bonjour daemon seems to have become annoying with polling nearby sleeping printers and log entries.

```shell
sudo systemctl disable avahi-daemon
```
