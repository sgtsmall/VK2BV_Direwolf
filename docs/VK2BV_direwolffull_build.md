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
  - Bitvise SSH Client
  - More here


For the install I am asuming you are using an ethernet connection and have reasonable internet access.

To start the process you just need the Pi plugged in.

login is: pi/raspberry

boots to sh (ssh available)

basic config stuff:


### Remove some software
This step is optional, however I currently have no need for this software and it significantly adds to the update times as the packages are very large. I'm not particularly concerned with saving the disk space just the download times.
The particular packages are the wolfram and libreoffice.
Start a terminal for these bits _Acessories/Terminal_ You may be able to do these through the WIMP's interface I'll probably find out one day! [Windows, Icons and Mouse Pointing]

```
sudo apt-get remove --purge wolfram-engine
sudo apt-get remove --purge libreoffice*
sudo apt-get clean
sudo apt-get autoremove
```

### Initial Setup

You can run the raspi-config from the menu _Preferences/Raspberry Pi Configuration_ or a command line.

```
sudo raspi-config
```

The Raspi-config is curses menu based uses arrow, tab and enter keys. The following options are what I would suggest changing.  
  
  
    
    -   expand filesystem  
    -   Internationalization/Change locale : en_AU.UTF-8  
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
