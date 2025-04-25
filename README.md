# Welcome to **Quill Smurf**, paraphrasing simplified.
Gif
# Features
* One-click paraphase an essay of any length.
* Select custom output directories.
* Produce clean, human-readable output.
* Show you how many copy-paste sequences saved.
# Usage Instructions
* Copy whatever body of text you are going to paraphrase.
* Paste that text into the application.
* Select an output directory (or hit enter to use the install directory as your output).
  * Currently, we only accept absolute paths for example:
    * C:\\\\User\\Username\\Downloads
  * Not:
    * .\\Downloads
* When run many instances of quillbot.com open up (in a headless firefox browser, so you won't see anything happening) and then paste in ~125 word segments of your input. 
* You will see each segment's paraphrased output in the application as each segment is completed.
* Once your entire essay is inputted into the paraphraser, find the "quillSmurfOutput.txt" file in your output directory for the final result.
# Installation
## 1. Necessary Dependencies 
Currently, QuillSmurf only works with the Firefox browser. Our binary ***should*** work with most recent Firefox version (tested up to v128.9.0esr), however if any issues arise as new Firefox updates appear, we will recompile those as needed.
## 2. Option A: Install Binaries (MOST USERS)
1. Click on the releases tab.
2. Download the source code .zip file.
3. Extract the .zip folder.
4. Open the folder and navigate to /dist/ and run the "main" application.
## 3. Option B: Compile from Source (Advanced Users)
Here is an install script for you (instructions are for debian based linux distros):

    sudo apt-get install python3
    pip install -U pyinstaller
    pip install -U nltk
    pip install -U selenium

    #OS Options : linux-aarch64, linux32, linux64
    export OS='INSERT OS NAME HERE'
    #Change this to whatever gecko driver version you want.
    export GECKO_DRIVER_VERSION='v0.36.0'
    
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-$OS.tar.gz
    tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-$OS.tar.gz
    rm geckodriver-$GECKO_DRIVER_VERSION-$OS.tar.gz
    chmod +x geckodriver
    cp geckodriver /usr/local/bin/

    pyinstaller main.py
    ./dist/main/main

Info on non-linux install will vary, check out [this resource](https://selenium-python.readthedocs.io/installation.html#drivers)

This script was based on [this stackoverflow thread](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu)
# Known Issues
## Indentation/formatting is not kept in the final output. (Low Priority)
Given that most essays are about 650 words on average, our bot will produce roughly 5 lines of output. In order to get back to original formatting, it will take on average 5 presses of the delete button, 5 presses of the enter button, and 5 presses of the tab button. For an average of 15 user inputs, it is currently not worth the complexity of tracking where user formatting originally was. Also, most users will lose their formatting when copy and pasting anyways so the amount of users pushing this change will benefit are slim. 