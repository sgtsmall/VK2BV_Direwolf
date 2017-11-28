VK2BV Direwolf - Build Full Image



# Build the Full Image

This document covers the Full image. It assumes you have a screen keyboard and mouse attached.

There is also a [lite image build document](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolflite_build.md) This starts with a network based command line.

From time to time you may need to completely rebuild the image. These instructions and some scripts represent a minimal set of installs and script changes that were needed to build the image. I ended up automating several of these steps and these notes are the result. Your mileage may vary!!!

# Parts for the full image

  - Tested with Raspberry Pi 2 to Raspberry Pi 3 (Using B+ model should work, have not tested with A models or zero)'
  - 8Gb SD card
  - Display (1024x768) (7") a seperate document will discuss smaller displays.
  - Keyboard, Mouse.
  - SoundBlaster USB Play Sound Card
  - Interface cable for your radio
  - 5V power for the Pi (initially it can be built from your PC USB, but later you will need around 2A [10W])
  - Optional
    - rPi interface board kit or the circuit can be assembled on any proto board.
    - GPS
    - RTC

For the Full image I recommend an 8Gb SD card (although 16Gb is fine)

I strongly recommend a Pi 3 here, the performance makes the experience much better.

If you are buying new then get a Pi 3. Note that Pi 3 has some issues with the way they have developed the bluetooth and some other components that make them not 100% compatible with more common Pi Hats, however this should not be a problem here.

Source for full image:

choose the raspbian full image.
or use the NOOBS build for raspbian

https://www.raspberrypi.org/downloads/raspbian/

There are several articles on how to create an image on the SD using these files.



_At this point you can build the system all plugged in. I personally do most of these steps initially via ssh because it is easier to cut and paste. I also get VNC going fairly early._

ssh software - it's builtin on most Mac and Linux. For windows
  - MobaXterm
  - Bitvise SSH Client
  - More here


For the install I am asuming you are using an ethernet connection and have reasonable internet access.

To start the process you just need the Pi plugged in.

### Latest Raspberry Jessie image does not enable ssh by default.

> To fix
> Option A:
> If you have a screen/keyboard attached
> On the 7" touch screen use Raspberry Menu/Preferences/Raspberry Pi Configuration/Interfaces  
>  SSH enabled  
> reboot  
>  
> Option B:
> after you have created the image load the sd card up on the pc again and you should get a disk volume called "boot".
> Open this drive in explorer/finder and create a file called ```ssh``` in the directory. In windows you can right click and create a text file saving as ssh (without the .txt)
> and then reboot with this image.
>


login is: pi/raspberry

boots to sh (ssh available)

basic config stuff:


### Remove some software
This step is optional, however I currently have no need for this software and it significantly adds to the update times as the packages are very large. I'm not particularly concerned with saving the disk space just the download times.
The particular packages are the wolfram and libreoffice.
Start a terminal for these bits _Acessories/Terminal_ You may be able to do these through the WIMP's interface I'll probably find out one day! [Windows, Icons and Mouse Pointing]

```
sudo apt-get -y remove --purge wolfram-engine
sudo apt-get -y remove --purge libreoffice*
sudo apt-get clean
sudo apt-get -y autoremove
```

### Initial Setup

You can run the raspi-config from the menu _Preferences/Raspberry Pi Configuration_ or a command line.

```
sudo raspi-config
```

The Raspi-config is curses menu based uses arrow, tab and enter keys. The following options are what I would suggest changing.  



    -   expand filesystem  
    -   Internationalization/Change locale : en_AU.UTF-8 and remove en_GB entry
    -     Select en_AU.UTF-8 as default
    -   Internationalization/Change timezone : AU/Sydney  
    -   advanced/hostname   : vkxxxpi  
    -   reboot  

After the reboot log in and we will install some software, first we refresh the repository and the system software.

```shell
sudo apt-get update
sudo apt-get -y upgrade
sudo reboot
```

Now we start with some installs, from here I am using apt-get -y to avoid the confirmation prompt

At this point you need to refer to the [lite image build](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolflite_build.md#support-for-soundcard-git-and-nslookup)

From the section
Support for soundcard, git and nslookup



That document will send you back here eventually


### Setting up icons and menus

If the other bits worked you should have a default desktop to run direwolf manually, however the steps in the other document show how to start it in the background anyway.

rest coming soon

## experimental YAAC gps

These notes are in progress.... your mileage may vary. I recommend for this you use a Pi3 or one of the other "large pi clones"

At about this stage having vnc working is handy for setup.
I like x11vnc, although by default the realvnc is available
there is also tightvnc

> sudo apt-get install x11vnc  
> x11vnc -storepasswd  

To run a session this can be started in the network ssh to get the main screen
> x11vnc -bg -nevershared -forever -tightfilexfer -usepw -display :0  

Running YAAC requires a keyboard and running a teminal from the Raspi sceen.

- use direswitch to configure as tnc with service enabled (and start it or reboot)
-
> cd  
> wget http://www.ka2ddo.org/ka2ddo/YAAC.zip    
> sudo apt-get -y install openjdk-7-jre librxtx-java unzip  
> mkdir YAAC  
> cd YAAC  
> unzip ../YAAC.zip  

From this point you need to be on the console screen

> java -jar YAAC.jar


> No APRS configured would you like help

Enter your callsign and select an SSID from the dropdown

choose an SSID different to what you entered in Direwolf... just in case.
Then next
Select Mobile and turn off Digi/I-gate for now
Select an icon
Then NEXT
for position choose Yes, via GPSD
...
For port choose AGWPE

localhost
8000

Transmit ... leave disabled for now

and here we open the worm can.... the screen is slightly too large you need to carefully move it up a bit to see the next button.

select enable station beacon and use gps
change text and Finish
Stop yaac and reboot

start yaac again and you should be receiving.

Go into the configure Expert mode  make it full screen and ports AGWPE set to transmit.

About now you need some maps. The default map connectors don't work so you need to download some stuff

You have to get pre built tiles

I downloaded a whole of australia file and ran the import function on another large debian workstation (you need a large amount of CPU, memory and disk -60GB to do this but the resulting files are only a few hundred MB) I will make the file available soon.

... more later including the install icons

OK I have built the icon command but not the right png files.

```
cd VK2BV_Direwolf
make install-rpi
cd
```

This will add some desktop icons and the YAAC.sh script
I actually recommend just using the menu entries under HamRadio or Other, rather than the desktop icon as it is hard to click.
