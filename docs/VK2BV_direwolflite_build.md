VK2BV Direwolf - Build Lite Image



# Build the Lite Image

This document covers the lite image. The lite image does not include the desktop components and is meant to be run via ssh access, network and or boot files.

There is also a [full image build](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolffull_build.md) This starts with the full desktop version. This opens a whole can of worms in its own right.

From time to time you may need to completely rebuild the image. These instructions and some scripts represent a minimal set of installs and script changes that were needed to build the image. I ended up automating several of these steps and these notes are the result. Your mileage may vary!!!

# Parts for the lite image

  - Tested with Raspberry Pi B+ to Raspberry Pi 3 (Using B model should work, have not tested with A models or zero)'
  - 8Gb SD card
  - SoundBlaster USB Play Sound Card
  - Interface cable for your radio
  - 5V power for the Pi (initially it can be built from your PC USB, but later you will need around 2A [10W])
  - Optional
    - rPi interface board kit or the circuit can be assembled on any proto board.
    - GPS
    - RTC

For the Lite image I recommend an 8Gb SD card (I often use 4Gb but they are hard to come by)
If you have an older Pi, I recommend at least a Pi B+ (the start of the micro SD ports and 4 x USB). However if you have a pi B that will work. I haven't tried with the 'A'.

If you are buying new then get a Pi 3. Note that Pi 3 has some issues with the way they have developed the bluetooth and some other components that make them not 100% compatible with more common Pi Hats, however this should not be a problem here.

Source for lite image:

choose the raspbian Lite image.

https://www.raspberrypi.org/downloads/raspbian/

There are several articles on how to create an image on the SD using these files. I don't recommend using NOOBS for this project. (If you have that in your kit set aside for now)

ssh software - it's builtin on most Mac and Linux. For windows
  - MobaXterm (this seems very good and the free limitations should not be a problem)
  - Bitvise SSH Client
  - More here in future


For the install I am asuming you are using an ethernet connection and have reasonable internet access.

### Latest Raspberry Jessie image does not enable ssh by default.

To fix, after you have created the image load the sd card up on the pc again and you should get a disk volume called "boot".
Open this drive in explorer/finder and create a file called ```ssh``` in the directory. In windows you can right click and create a text file saving as ssh (without the .txt)




To start the process you just need the Pi plugged in.

login is: pi/raspberry

boots to sh (ssh available)

basic config stuff:


### Initial Setup

```
sudo raspi-config
```

The Raspi-config is curses based menu,  uses arrow, tab and enter keys, space bar to de/select options. The following options are what I would suggest changing.



    -   expand filesystem
    -   Internationalization/Change locale : en_AU.UTF-8 and remove en_GB entry
    -     Select en_AU.UTF-8 as default
    -   Internationalization/Change timezone : AU/Sydney
    -   advanced/hostname   : vkxxxpi
    -   reboot

After the reboot log in and we will install some software

```shell
sudo apt-get update
sudo apt-get -y upgrade
sudo reboot
```

Now we start with some installs, from here I am using apt-get -y to avoid the confirmation prompt

### Support for soundcard, git and nslookup

full_build users can follow these steps in a console(x-terminal)

```
sudo apt-get -y install libasound2-dev git-core dnsutils gawk automake libtool
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

### Clone these documents and script files
```shell
cd ~
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build
```
### Install and build hamlib
 This is not strictly necessary unless you are dealing with a radio that uses it. But it is a good exercise of your system, if you build it now it will be available to the direwolf build.

```shell
wget https://sourceforge.net/projects/hamlib/files/hamlib/3.0.1/hamlib-3.0.1.tar.gz
tar -zxf hamlib-3.0.1.tar.gz
mv hamlib-3.0.1 hamlib
cd hamlib
./configure --with-xml-support --with-python-binding
make
make check
sudo make install
sudo reboot
```

### Now we get direwolf



```
cd ~
git clone https://www.github.com/wb2osz/direwolf
cd direwolf
make
sudo make install
make install-conf

#If you are building a full display version also run the next command
make install-rpi
#This step created a desktop icon for Direwolf

cd ~
```

So now direwolf is installed but not yet configured.



## configure alsa (Sound card)

Need more detail here but basically you use the command

```
alsamixer
```

This gves you a curses based application for the soundcard. By default it is pointing at the sound card within the Pi. You need to use F6 to select the USB device.

If you look at the top left you are likely in F3: Playback

Speaker, Mic, AGC

The Mic you see here is a Mic Monitor level.
Use F5: All to see both output and input.

You should get
Speaker, Mic [Monitor], Mic and AGC

OutputSpeaker and Mic input should be set around 50%. Use up/down arrows
Mic Monitor should be muted MM use M key.
AGC should be off as well [M].

The settings are automatically saved on exit.


## Configure direwolf

By default direwolf creates a file  direwolf.conf  in the home directory, this contains the information you need to create most configs. I have included a script that will gather some details and create a new file called direwolf.sample.

first of all keep a copy of the default direwolfconfig

```shell
cd ~
mv direwolf.conf direwolf.origconf
```

I have included a script that will gather some details and create a new series of files for different usage.



# Testing the RPi board and GPIO ports

Make sure wiringpi is installed and you should have the gpio program available

```
gpio readall
```

Should produce a table of gpio pin information for your RaspberryPi
Numbering...
So this table shows there are many sets of numbers to reference the pins.

The pin numbers 1 to 40 are referred to as the board number.
The wPi number is an attempt to refer to the pins by GPIO number.
The BCM number stands for Broadcom(BCM) SOC Channel.

Direwolf (and fldigi)  refers to the BCM Number

The connection that I prefer is to use a strip of 10way IDC cable attached from physical pins 11-20 on the 50way header.
I then use:
> 11,12,13 - No connect
> 14 - Gnd
> 15 - GPIO22 (BCM Number)
> 16 - GPIO23 (BCM Number)
> 17 - 3.3V
> 18,19,20 - No Connect

These 4 cables conveniently line up with the RPi board

> 14 <-> gnd
> 15 <-> ptt
> 16 <-> dcd
> 17 <-> 3.3v


To test the pinouts - ensure direwolf shutdown, radio disconnected.

```
gpio -g mode 22 out
gpio -g mode 23 out
#now test
#dcd LED on
gpio -g write 23 1
#dcd LED off
gpio -g write 23 0
#ptt LED on
gpio -g write 22 1
#ptt LED off
gpio -g write 22 0
```

If things are switching on and off it is time to test and set the ptt timeout pot.
issue the ptt (gpio -g write 22 1) on command and time how long before ptt LED goes off,
now issue the ptt off.
Adjust the pot and repeat until you get to 20 seconds for most usage. (That is a fairly long transmission, however if you are going to use other digital modes you may need longer [JT65 50 seconds])

Finally connect the radio and you should see ptt come on and off by command above.

## Testing direwolf

```
cd ~
direwolf -t 0
```

This should read /home/pi/direwolf.conf and start up (-t 0 turns off the colour outputs)

## Configuring direwolf as a service

If you want direwolf to always run on startup then we should configure as a service. Scripts and files for this are contained in the github, although it is recommended to do refresh your git to make sure you have the latest.
If it has been sometime since you last installed these scripts then refresh them, otherwise next step.

```
cd ~
cd VK2BV_Direwolf
git pull
sudo make install
cd ~
```

This should copy the relevant files in place.

Documentation about the scripts and the order of use is here [VK2BV direwolf scripts](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolf_scripts.md) document section

You can use the diremenu commands to enable and disable the service

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

recent log of activity

Use menu option i) sudo systemctl enable direwolf.service  
to enable startup after reboots




Full_build (displays) should now go back to the [full image build](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolffull_build.md#setting-up-icons-and-menus) document section

Setting up icons and menus


# Extra Pieces

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
