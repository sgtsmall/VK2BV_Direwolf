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

<table>
  <tr>
    <td>sudo raspi-config</td>
  </tr>
</table>
The Raspi-config is curses menu based uses arrow, tab and enter keys. The following options are what I would suggest changing.  
  
  
    
    -   expand filesystem  
    -   Internationalization/Change locale : en_AU.UTF-8  
    -   Internationalization/Change timezone : AU/Sydney  
    -   advanced/hostname   : vkxxxpi  
    -   reboot  

After the reboot log in and we will install some software
<table>
  <tr>
    <td>sudo apt-get update<br>
sudo apt-get upgrade<br>
sudo reboot</td>
  </tr>
</table>

Now we start with some installs, from here I am using apt-get -y to avoid the confirmation prompt

### Support for soundcard, git and nslookup
<table>
  <tr>
    <td>sudo apt-get -y install libasound2-dev git-core dnsutils gawk</td>
  </tr>
</table>

### gpsd install
This next section is to support gps attached to the Pi, even if you don't have the gps you can install this now and it will build in the right bits for later.
<table>
  <tr>
    <td>
sudo apt-get -y install gpsd libgps-dev</td>
  </tr>
</table>

#### optional git settings - not sure if these are needed
These entries may not be needed for most interactions with git so dont enter yet (unless git prompts you for the information)<br>
  - git config --global user.name “vkxxx"<br>
  - git config --global user.email xxx@xxx.com<br>

### Install and build hamlib 
 This is not strictly necessary unless you are dealing with a radio that uses it. But it is a good exercise of your system, if you build it now it will be available to the direwolf build.

<table>
  <tr>
    <td>
cd ~<br>
git clone git://hamlib.git.sourceforge.net/gitroot/hamlib/hamlib<br>
cd hamlib<br>
sh autogen.sh --with-xml-support --with-python-binding<br>
make<br>
make check<br>
sudo make install<br>
sudo reboot
</td>
  </tr>
</table>

### Now we get direwolf

We are using some extra commands here git tab will list the versions available in the git repository, git checkout will select the one we want _currently 1.3_.

<table>
  <tr>
    <td>
cd ~<br>
git clone https://www.github.com/wb2osz/direwolf<br>
cd direwolf<br>
git tag<br>
git checkout 1.3<br>
make<br>
sudo make install<br>
make install-conf</td>
  </tr>
</table>

So now direwolf is installed but not yet configured.

## todo configure gpsd
## todo configure alsa
## todo configure direwolf


