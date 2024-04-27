# Notice

This is a toy script glued together using snippets from Google Gemini made for a friend to prove a point.

Please do not use it for real work.

It's a Python script that takes in flags to compare 2 separate images. It will resize the smaller image to the same dimensions as the large image, adjust the brightness to match as much as possible before doing a diff using OpenCV. The delta image will be dumped out as a result.

You may tweak the threshold to highlight more or less differences, but I've found 5 - 10 a pretty good range.


# How to use the script

You first need the [Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html). It's a piece of software that reads the Python script and execute actions based on it. To do that, you can either install it directly, or you could use a nifty terminal tool called [Homebrew](https://brew.sh/) to install it for you. Think of Homebrew as an installer manager for terminal command line software. You can use it to install, update, upgrade command line software. Technically speaking you can also use it to install GUI software, but just use the macOS Application manager to do that instead.

## Install Homebrew

Open Terminal and run the following:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

`curl` is a command that sends an HTTP request. It's essentially downloading the `install.sh` file onto your Mac. `/bin/bash` is an environment to run terminal commands. There are many others like the default `sh`, or `zsh`, `fish`. But the most widely used one is `bash`.

Essentially the command is downloading `install.sh`, a bash script, and running it with your Mac's bash shell to install Homebrew.

## Use Homebrew to install Python

Once Homebrew is installed, run:

```
brew install python3
```

`brew` is the Homebrew software manager (package manager) you just installed. You are using it now to install the latest version of Python 3.

## Install Python packages that the image compare script uses.

I imported some prewritten Python code elsewhere (called libraries) to use in the script. You need to have these libraries on your computer so that the script can import them when it's being run by the Python Interpreter.

To do this type into your Terminal:

```
python3 -m pip install opencv-python absl-py
```

`pip` is Python3's very own package manager. Just like how Homebrew manages software packages for your macOS, `pip` manages software libraries for your Python3 environment. You run it as a module within Python itself, thus `python3 -m pip`.

You are using it to install 2 libraries used in my compare script.

`opencv-python`: A very popular computer vision library that can do all sorts of image processing magic in Python.

`absl-py`: A library with a lot of standard tools. I use it just to run the script like an app, and read command line flags.

## Time to test!

### 1. Create the test files and compare script

In your macOS GUI go to any directory of your choice and dump in 2 images that you want to compare. Then create a text file, and compare in all the contents in `compare.py`. Rename the text file to `compare.py`.

### 2. Find the full directory path to yoour test directory

In the Finder directory, go to the menu toolbar on top and click `View` > `Show Path Bar` to display the directory to your current directory. Right click on the directory name and click `Copy <directory> as Pathname`. You now have the complete directory path to where your images and the `compare.py` script is.


### 3. Run the script!

Go to Terminal again and type:

```
cd <full directory path you copied>
```

`cd` means `change directory`, i.e. open folder.

Run the script against your images.

```
python3 compare.py --image1=first_image.jpg --image2=second_image.jpg --output=diff.jpg --threshold=10 --adjust_brightness=1
```

Replace the flag values for `image1` and `image2` with your test image filenames. The difference should be dumped out in a new `diff.jpg` file. You can tweak the `threshold` flag value from 0 to any positive amount, but 5 - 10 has worked well enough in my testing.

`adjust_brightness` is turned on by default. It adjusts the brightness of the images to match each other as much as possible so that we don't identify differences in pixel because one image is brighter. If you do want to detect brightness difference, then set the flag to 0.
