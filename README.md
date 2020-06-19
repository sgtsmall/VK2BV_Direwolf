# VK2BV_Direwolf
Scripts and documentation to build Direwolf Raspberry Pi iGate-Beacon-Digipeater-TNC.
This Github entry is not finalised... stuff is still all over the place.




## Overview
*   Using most Raspberry Pi's with a USB soundcard and GPIO based adapter board to create a TNC that can support several APRS functions.

*   **OR now you can use a standard RTL-SDR type dongle to make a simple iGate.**

>  * Note: for these projects I used to recommend a SoundBlaster Play USB (original) I haven't tried the Soundblaster Play 2 yet but I expect it to work, now there are sufficient drivers around for most of the cheap USB sound dongles that used to be a problem
> *  I have also had success with some early Logitech Headset USB adapters.

*   My common setup with this is a Raspi B+ with the soundcard and
  *       UV-5R and purpose built cable to support Audio In/Out and PTT. To power it I use an Ebay 12+V to 5V USB adapter module and the battery eliminator module for the 5R.
  *       Yaesu/iCom Mobile Rig with 6 pin data cable to support Audio In/Out and PTT.

***

**Important:** These guides expects you to have a more than basic grasp of the Linux command line. In order to follow it you'll need to know:

  * how to issue commands on the shell,
  * how to edit a text file from the command line,
  * what the difference is between your user account (e.g. `pi`) and the superuser account `root`,
  * how to SSH into your Pi (so you don't need to also attach keyboard and monitor),
  * how to use Git and
  * how to use the Internet to help you if you run into problems.

This is **not** a "Linux for Beginners guide", those can be found for example [here](http://elinux.org/RPi_Beginners) and [here](http://linuxcommand.org/learning_the_shell.php). For some Git basics please take a look [here](http://rogerdudler.github.io/git-guide/).

***  



## Installation

Follow the full install guides linked below for the full process. To just install these scripts:

```shell
git clone https://github.com/sgtsmall/VK2BV_Direwolf.git
cd VK2BV_Direwolf
make
sudo make install
cd ~
diremenuup
```
#### After installing this package, running diremenuup will now install the components to the right directories and apt-get additional needed packages.



There are 3 build versions here.

* SDR build
* lite build (no display)
* Full build including some parts to improve the display.

The bit I have added is a set of scripts to go through some of the troubleshooting and configuring startup.

Most, (98%), of this information is taken from the direwolf configuration documents. One of the steps you perform in the install notes below is downloading the direwolf package to the Pi, this contains all the basic direwolf code and documents.
  > Although this process downloads everything to the Raspberry pi, you should probably download the direwolf package to your pc as well for easy access to the doc folder that has lots of information.
Go to the github site and download the project as a zip file, from there you can get to the documents located in the doc directory.

https://github.com/wb2osz/direwolf

### VK2BV build instructions

The SDR version creates a very low cost iGate for receiving beacons and putting out to the internet.
I recommend the lite version to start with particularly for beacons, digipeaters or SARTrack.

I also recommend starting again if you build a "full" version. It's not hard and takes a lot less fiddling around than adding the Desktop later.

* SDR - build a version using an SDR dongle for iGate [SDR build instructions link](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolfsdr_build.md)

* Lite - full featured direwolf device can be used as beacon, tnc, digipeater, tracker, ... [Lite build instructions link](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolflite_build.md)

* Full - All the function of Lite, with some information on running on the pi desktop with vnc or monitor/keyboard [Full  build instructions link](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolffull_build.md)

I have moved the information about the local scripts, diremenu, diresetup, .... to this document

* [VK2BV_direwolf scripts link](https://github.com/sgtsmall/VK2BV_Direwolf/blob/master/docs/VK2BV_direwolf_scripts.md)


## Documentation

There will be lots of documentation here: https://github.com/sgtsmall/VK2BV_Direwolf/tree/master/docs (oneday)

## Support

ideas and questions can be handled on the http://vk2bv.org website soon

## Videos

Maybe

## Configuration Tool

Later

## Contributing

Contributions are welcome and encouraged.  You can contribute in many ways:

* Documentation updates and corrections.
* How-To guides - received help?  help others!
* Bug fixes.
* New features.
* Telling us your ideas and suggestions.

Next place is the github issue tracker:

https://github.com/sgtsmall/VK2BV_Direwolf/issues

Before creating new issues please check to see if there is an existing one, search first otherwise you waste peoples time when they could be coding instead!

## Developers

Please refer to the development section in the `docs/development` folder.


## VK2BV Direwolf Releases
https://github.com/sgtsmall/VK2BV_Direwolf/releases
