
# Description

This repo contains the code for some simple webscraping+interaction. Its purpose is to book automatically classes slots for the University of Trieste's web service.

# Installation Instructions

Since this bot is a very fast-built command-line interface, I shall provide the steps to ensure a smooth functioning for non-technical users.

The bot uses `Python`, so a Python installation on your computer (Linux, Mac, Windows) is required. If you do not have one, or you have the "system default" installation and have never even bothered to touch it, I suggest to install (**`Python` with Anaconda**)[https://www.anaconda.com/products/individual]. Once installed, either create a custom virtual environment ((here's)[https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html] the documentation for what they are) or use the standard one, I could not care less.

Once you have a somewhat working `Python` installation, it is then the time to install all of the requirements. To do so, just to `pip install -r requirements.txt` (you can find the file in the root of the repo). If 

The program also uses **Google Chrome**, and thus please install it on your machine as well. In order to have the *automation*, you are also required to install on your machine `chromedriver`. To do so, plase visit the (download page)[https://chromedriver.chromium.org/downloads] and download the `chromedriver` corresponding to your **Google Chrome** version and operating system.
Once downloaded, place the `chromedriver` file in the root folder of the repo.

# Manually Run

In order to run the program in the current moment, once you have installed everything as instructed (please do!), just run **from the root of the repo**:
```
python src/run/run_place_selection.py
```
and follow the instructions. If everything goes okay, you will see printed `'#### PROGRAM TERMINATED ####'`. If you don't, either you forgot to install something or you found a bug in the program: for the former, just install please; but, if the latter is the case, please open an issue in the repo and I will try to fix it.

# Create Scheduled Run

Now, this is where the fun begings. The best way to have a scheduled run of a program in Unix-like systems, that is most likely *MacOS* and *Linux* is to use `cron`. To scheduled the program, just to `crontab -e` and then, in the open editor, write a new line with 
```0 22 * * * python /path/to/AlfyBooker/src/run/run_place_selection.py```

If you are using *Windows*, first off plase do not! Secondly, there is some command line tool for it, but I do not feel like learning it: see [here](https://ss64.com/nt/schtasks.html).

@Leonardo Alchieri, 2021
