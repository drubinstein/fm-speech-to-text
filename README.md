# FM-SDR

RTLSDR processing software primarily geared at processing and analyzing FM

## Getting Started

 These instructions will get the software running on your local machine

 Install RTLSDR drivers for your machine. I recommend following the quickstart
 guide from https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/.

 To install necessary python requirements run:
 `pip install -r requirements.txt`

 In addition, if you are on Windows, there are additional dlls you must install
 manually as per the instructions from pyrtlsdr (https://github.com/roger-/pyrtlsdr). What I
 personally had to do:
 1. Download the appropriate zip from https://github.com/librtlsdr/librtlsdr/releases
 2. Extract the zip to some directory
 3. Take the \*.dll files from the extracted directory and place them in this
    folder*

\* I will try to write a script that does that for you in the future.
