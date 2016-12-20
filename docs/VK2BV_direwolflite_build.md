VK2BV Direwolf - Build Lite Image



# Build the Lite Image

This document covers the lite image. The lite image does not include the desktop components and is meant to be run via ssh access, network and or boot files.

There is also a full image build (https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolffull_build.md) This starts with the full desktop version. This opens a whole can of worms in its own right.

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
  - Bitvise SSH Client
  - More here


For the install I am asuming you are using an ethernet connection and have reasonable internet access.

To start the process you just need the Pi plugged in.

login is: pi/raspberry

boots to sh (ssh available)

basic config stuff:


### Initial Setup

```
sudo raspi-config
```

The Raspi-config is curses menu based uses arrow, tab and enter keys. The following options are what I would suggest changing.



    -   expand filesystem
    -   Internationalization/Change locale : en_AU.UTF-8
    -   Internationalization/Change timezone : AU/Sydney
    -   advanced/hostname   : vkxxxpi
    -   reboot

After the reboot log in and we will install some software

```shell
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```

Now we start with some installs, from here I am using apt-get -y to avoid the confirmation prompt

### Support for soundcard, git and nslookup

```
sudo apt-get -y install libasound2-dev git-core dnsutils gawk
sudo apt-get install  automake libtool
```


### gpsd install
This next section is to support gps attached to the Pi, even if you don't have the gps you can install this now and it will build in the right bits for later.

```
sudo apt-get -y install gpsd libgps-dev
```

#### optional git settings - not sure if these are needed
These entries may not be needed for most interactions with git so dont enter yet (unless git prompts you for the information)<br>
  - git config --global user.name “vkxxx"<br>
  - git config --global user.email xxx@xxx.com<br>

### Clone these documents and script files
```shell
cd ~
git clone git://github.com/sgtsmall/VK2BV_direwolf
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build
```
### Install and build hamlib
 This is not strictly necessary unless you are dealing with a radio that uses it. But it is a good exercise of your system, if you build it now it will be available to the direwolf build.

```shell
cd ~
git clone git://hamlib.git.sourceforge.net/gitroot/hamlib/hamlib
cd hamlib
sh autogen.sh --with-xml-support --with-python-binding
make
make check
sudo make install
sudo reboot
```

### Now we get direwolf

We are using some extra commands here, git tab will list the versions available in the git repository, git checkout will select the one we want _currently 1.3_.

```
cd ~
git clone https://www.github.com/wb2osz/direwolf
cd direwolf
git tag
git checkout 1.3
make
sudo make install
make install-conf
```

So now direwolf is installed but not yet configured.

## todo configure gpsd
## todo configure alsa
## todo configure direwolf

By default direwolf creates a file  direwolf.conf  in the home directory, this contains the information you need to create most configs. I have included a script that will gather some details and create a new file called direwolf.sample.

first of all keep a copy of the default direwolf.config

```shell 
mv direwolf.conf direwolf.origconf
```


To get started a simple script has been created that will generate a file direwolf.sample this creates several config entries that can be used. Some should be deleted or commented, more infor required here....

```shell
cd ~
VK2BV_direwolf/bin/configdirew
```

Sample here [find a new markdown for screen sample]
Note the format for lat and lon

```
Params are Callsign NOCALL Terminal 1 creating NOCALL-1
 APRSIS passcode 12345
lat is 33^51.43S  lon is 151^12.91E
gpio BCM DCD 23  PTT 22 

Valid Callsign [e.g. VK2ABC] [NOCALL]VK2ABC
Terminal number [e.g. 1] [1]
Passcode is unique for your Callsign 
Passcode for [VK2ABC] calculated as [21931] 
APRSIS Passcode number [21931]
lat and long for your igate location
Format is deg^MM.MMS  use the aprs.is google map to get the value
lat value [e.g. 33^51.12S] [33^51.43S]
lon value [e.g. 151^51.12E] [151^12.91E]
GPIO pin selection
Uses the BCM number for the PTT signal and DCD
ptt value [e.g. pin 15 BCM 22] [22]
dcd value e.g. pin 14 BCM [23]
Params are Callsign VK2ABC Terminal 1 creating VK2ABC-1
 APRSIS passcode 21931
lat is 33^51.43S  lon is 151^12.91E
gpio BCM DCD 23  PTT 22 

 If the values are correct enter Y  [n]Y
```

This generates the sample file
```
 #device
 ADEVICE plughw:1,0
 ACHANNELS 1
 #channel
 CHANNEL 0
 MYCALL VK2ABC-1
 MODEM 1200
 PTT GPIO 22
 DCD GPIO 23
 AGWPORT 8000
 KISSPORT 8001
 #Fixed Position Beacon
 PBEACON delay=1  every=30 overlay=S symbol="digi" lat=33^51.43S long=151^12.91E power=10 height=20 gain=4 comment="Test Direwolf Node"
 #Digipeater
 DIGIPEAT 0 0 ^WIDE[3-7]-[1-7]$|^TEST$ ^WIDE[12]-[12]$ TRACE 
 #Igate
 IGSERVER sydney.aprs2.net
 IGLOGIN VK2ABC-1 21931
 PBEACON sendto=IG delay=0:30 every=60:00 symbol="igate" overlay=R lat=33^51.43S long=151^12.91E 
```
copy this file to direwolf.conf and edit
I suggest commenting out the PBEACON and DIGIPEAT statements initially until the receiver mode is running

```
cp direwolf.sample direwolf.conf
```

Longer discussion on configs here





### Testing the RPi board and GPIO ports

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
11,12,13 - No connect
14 - Gnd
15 - GPIO22 (BCM Number)
16 - GPIO23 (BCM Number)
17 - 3.3V
18,19,20 - No Connect

These 4 cables conveniently line up with the RPi board

14 <-> gnd
15 <-> ptt
16 <-> dcd
17 <-> 3.3v


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

### Testing direwolf

```
cd ~
direwolf -t 0
```

This should read /home/pi/direwolf.conf and start up (-t 0 turns off the colour outputs)

### Configuring direwolf as a service

If you want direwolf to always run on startup then we should configure as a service. Scripts and files for this are contained in the github, although it is recommended to do refresh your git to make sure you have the latest.

```
cd ~
cd VK2BV_direwolf
git pull
cd bin
sudo sh -x direwolf.install
cd ~
```
This should copy the relevant files in place.
To start manually 
sudo service start direwolf.service









### Fixed IP Address on the new raspbian since jessie

The fixed ip address information is now located in /etc/dhcpcd.conf

This creates a static entry 192.168.5.50

```
interface eth0
static ip_address=192.168.5.50/24
static routers=192.168.5.1
# static domain_name_servers=8.8.8.8
```

