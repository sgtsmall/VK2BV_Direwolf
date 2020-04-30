VK2BV Direwolf - script files for setup and debug



# Using the scripts and menus

The following install section adds some local scripts to the programs and installs the service files for direwolf in the background. This also generates desktop files for the Full image. Additional commands are needed to start the background job.

```shell
git clone https://github.com/sgtsmall/VK2BV_Direwolf.git
cd VK2BV_Direwolf
make
sudo make install
cd ~
```

This will add some desktop icons and the YAAC.sh script
I actually recommend just using the menu entries under HamRadio or Other, rather than the desktop icon as it is hard to click.

This installs some basic command scripts, the scripts show what command they are using.

#### TL;DR Getting started

- Find your lat/lon from google maps or just use the default, you will need "deg mm.mm N/S" (e.g. "33^51.43S" is Sydney), your callsign, and SSID (e.g. 1) and the gpio pins. - Just use defaults if needed, the purpose of the script is to show the structure to get started.  
- run diremenu from cmd line.
- opt c) direconfig
	- answer the questions
- opt d) direswitch
	- opt g) copy samples
	- you have to type Y to each line (safety precaution in case you have customised your own files.)
	- opt l) link pbeacon
	- Now you have an example beacon in your config.
	- opt q) - to quit this menu
- opt e) diresetup
	- you now have access to adjust/test GPIO, direwolf, GPS.


### diremenu

Diremenu is a very simple script that displays some commands and executes them when the letter is typed with return.

It will try and run the command as seen, there is no validation or checking if you are in the right directory (almost always expects $HOME ). It is provided to get you started and to see some of the commands you should use.

- check the outputs
- run other menus
- stop/start/enable/disable service
- updates VK2BV_Direwolf scripts


### direconfig

This script asks some basic questions and creates a set of sample config files. The logic is minimal but should get you started, you should edit the files for more settings when you are ready.

- needs lat/lon in format for APRS note DD^MM.MMS
- Callsign (Script will calculate your APRS passkey)
- SSID for APRSIS/transmits
- GPIO numbers for PTT and DSD


### direswitch

This script is used to create a link between different setups and a common direwolf.conf file.
This is especially useful if you are running direwolf as a service (see below) such that you can choose the startup after the next boot.

As a worked example, I usually run the unit just as a (direwolf.conf.tnc) TNC that I can connect to SARTrack or other software (YAAC - Yet Another APRS Client) It doesn't beacon itself. Then I may set it as a fixed position beacon (direwolf.conf.pbeacon) for a while. Later I may use it as a tracker (direwolf.conf.gbeacon) or as a digipeater (direwolf.conf.digi)

### diresetup

This script contains most of the one off commands used during the setup process. Rather than constantly scrolling through the notes I put them together.

Things like the gpio commands the gpsd commands and a new feature direwolf -x and a direwolf test beacon, are arranged in 3 sub menus.

As the script highlights you need to have run the direconfig and copied the sample configs with direswitch.

```
Direwolf Test menu

a) direwolf -t 0 -x -c direwolf.conf
```

Will transmit a test tone to the radio to help with levels (listen with another radio for overmodulation).

```
b) link testbeac

e) direwolf -t 0 -c direwolf.conf
```

Will transmit a fixed beacon after 30 seconds every 30 seconds. You should also see decoded packets.

####
GPS Menu
To check if the gps is sending data you need to stop the background, start gpsd sock, run cgps, then kill the gpsd and restart the background.

```
GPS Menu
a) sudo systemctl status gpsd.socket
b) sudo systemctl stop gpsd.socket
c) sudo gpsd /dev/ttyACM0 -F /var/run/gpsd.sock
d) cgps
e) sudo killall gpsd
f) sudo systemctl start gpsd.socket
```


## configure gpsd

I moved this section here because the new diresetup menu has all these commands.

The USB style GPS units should come up on port /dev/ttyACM0
some troubleshooting hints are [here](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=123989)

The earlier install of the gpsd software, should have created the service entries for gpsd.

Check the status

```
sudo systemctl status gpsd.socket
```

Stop the services

```
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
```

Starting the gps manually

```
sudo gpsd /dev/ttyACM0 -F /var/run/gpsd.sock

gpsmon
[Ctrl-C to quit]
```

If you have finished testing gpsd interactively then kill the running process (or just leave it, you will be able to enable the background startup but not start it, because it is already running)

Edit the defaults file for startup

> sudo nano /etc/default/gpsd  
> ...  
> DEVICES="/dev/ttyACM0"  
> ...  
> GPSD_OPTIONS="-F /var/run/gpsd.sock"  

```
sudo killall gpsd
```

Start the services

```
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket
```


## Sample Configurations

Use the command direconfig or select from the diremenu option

```shell
direconfig
```

Configuration examples
This is a simple text menu that will prompt for entries. The default entry is shown in brackets.
If you make a mistake you can rerun the command or just go around the entries again until correct.

Note the format for lat and lon


> Params are Callsign NOCALL Terminal 1 creating NOCALL-1  
> APRSIS passcode 12345  
> lat is 33^51.43S  lon is 151^12.91E  
> gpio BCM DCD 23  PTT 22   
>   
> Valid Callsign [e.g. VK2ABC] [NOCALL]VK2ABC  
> Terminal number [e.g. 1] [1]  
> Passcode is unique for your Callsign   
> Passcode for [VK2ABC] calculated as [21931]   
> APRSIS Passcode number [21931]  
> lat and long for your igate location  
> Format is deg^MM.MMS  use the aprs.is google map to get the value  
> lat value [e.g. 33^51.12S] [33^51.43S]  
> lon value [e.g. 151^51.12E] [151^12.91E]  
> GPIO pin selection  
> Uses the BCM number for the PTT signal and DCD  
> ptt value [e.g. pin 15 BCM 22] [22]  
> dcd value e.g. pin 14 BCM [23]  
> Params are Callsign VK2ABC Terminal 1 creating VK2ABC-1  
>  APRSIS passcode 21931  
> lat is 33^51.43S  lon is 151^12.91E  
> gpio BCM DCD 23  PTT 22  
>  
> If the values are correct enter Y  [n]Y  

Sample files are now in $HOME/dconf/sample

This generates the sample files.
They all start with this section:

> \# device  
> ADEVICE plughw:1,0  
> ACHANNELS 1  
> \# channel  
> CHANNEL 0  
> MYCALL VK2ABC-1  
> MODEM 1200  
> PTT GPIO 22  
> DCD GPIO 23  
> \# Network TNC  
> AGWPORT 8000  
> KISSPORT 8001  

They then finish with different tail sections

> \# Fixed Position Beacon  
> PBEACON delay=1  every=30 overlay=S symbol="digi" lat=33^51.43S long=151^12.91E power=10 height=20 gain=4 comment="Test Direwolf Node"  

> \# Tracker  
> GPSD  
> SMARTBEACONING 50 2:00 5 15:00 0:15 20 255

> \# Digipeater   
> PBEACON delay=1  every=30 overlay=S symbol="digi" lat=33^51.43S long=151^12.91E power=10 height=20 gain=4 comment="Test Direwolf Node"  
> \#  
> DIGIPEAT 0 0 ^WIDE[3-7]-[1-7]$|^TEST$ ^WIDE[12]-[12]$ TRACE  

> \# Igate  
> IGSERVER sydney.aprs2.net  
> IGLOGIN VK2ABC-1 21931  
> PBEACON sendto=IG delay=0:30 every=60:00 symbol="igate" overlay=R lat=33^51.43S long=151^12.91E

## Switching startups

```shell
direswitch
```

This command now supports, cat the config, linking, stop and restarting the service

> a) ls -al /home/pi/dconf/*conf*   
> b) cat /home/pi/direwolf.conf  
> c) direconfig  
> d) sudo service direwolf stop  
> e) sudo service direwolf start  
> f) sudo service direwolf restart  
> g) copy samples to config directory  
> h) link tnc  
> i) link digi  
> j) link igate  
> k) link gbeacon  
> l) link pbeacon  
> m) link custom  
> n) direwolf -t 0 -c direwolf.conf  
> q) quit this menu  

In particular:
Use option c) to rebuild your config file with a different location. This will only put the ouput into the sample directory ($HOME/dconf/sample/).
Use option g) to copy the samples into the configuration directory. The prompt is looking for 'Y' to perform the copy.
option h) links the network tnc mode. This is useful to start testing receive.


## Basic Menu

```shell
diremenu
```

This is some basic commands, the menu uses the actual commands as prompts, more as reminders of what you may need to do.

> a) tail -f $HOME/direwolf.output  
> b) ls -al $HOME/direwolf.conf  
> c) direconfig  
> d) direswitch
> e) diresetup
> f) sudo service direwolf stop  
> g) sudo service direwolf start  
> h) sudo service direwolf restart  
> i) sudo service direwolf status  
> j) sudo systemctl enable direwolf.service  
> l) sudo systemctl disable direwolf.service  



command i) enable and j) disable are used to start and stop direwolf restarting after a boot.

command a) is used to monitor the output of the direwolf job.
