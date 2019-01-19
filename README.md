# Intro
This repository includes python scripts I've created for personal use. 

# Crontab updater
I have created python scripts to help automate updating /etc/crontab on my CentOS machines. I've written 2 scripts, one for python 2.7.x, and one for python 3.6.x. When executed, the script searches for certain strings. If no matching string is found, an entry will be added to /etc/crontab.

You can modify the scripts to update other text files also. 

## crontab-updater-py27.py
- Use on CentOS 7 to update /etc/crontab idempotently.
- This adds 3 entries into /etc/crontab, but only if certain condition is met.
- Works with python 2.7.5, default version found on CentOS 7.

## crontab-updater-py36up.py
- Use on CentOS 7 to update /etc/crontab idempotently.
- This adds 3 entries into /etc/crontab, but only if certain condition is met.
- This script works with python 3.6.5 and above. Specifically tested with 3.6.5 and 3.7.1.
- This script will not work with Python 2.7.5, default python version found on CentOS 7.
- In my environment, I use pyenv and pipenv to run python version 3.6.5 on CentOS 7. The specific command I run is below:

    ```
    cd ~/env/gp01-3.6.5 && pipenv run sudo ~/.pyenv/shims/python ~/bin/crontab-updater-py36up.py
    ```
- You'd need to be familiar with pyenv and pipenv to use crontab-updater-py36up.py. If you are not, you can use crontab-updater-py27.py instead.
