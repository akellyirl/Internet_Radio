# Internet_Radio
Arduino / Raspberry Pi Internet Radio

This is a project for Arduino and Raspberry Pi to make an Internet Radio, aimed at intermediate skill level. Some familiarity with Linux usage will be beneficial (or access to someone who can help out if required).

Raspberry Pi runs mpd music player daemon to receive and decode the internet radio stream.
ALSA running on the Raspberry Pi provides the sound through either the Jack Socket or the HDMI output.

Arduino runs a nanpy interface code to interface with Python, providing Text output of the Radio Station playing and Button inputs to control Playback.

Objectives:
* Learn how to use the mpd/mpc on the Raspberry Pi
* Learn how to use the nanpy library for Python to interface the Pi to the Arduino
* Make a Cool Internet Radio

For all the details take a look here: http://www.akellyirl.com/how-to-make-an-arduino-raspberry-pi-internet-radio/

FILES:
radio.py        : basic Python radio code
radio_jazzi.py  : Improved Python radio code
