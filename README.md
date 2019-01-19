# Intro
This repo includes python scripts I've created for personal use. 

# Files

## crontab-updater-py27.py
- Use on CentOS 7 to update /etc/crontab idempotently.
- This make 3 entries into /etc/crontab, but only if certain condition is met.
- Works with python 2.7.5, default version found on CentOS 7.

## crontab-updater-py36up.py
- Use on CentOS 7 to update /etc/crontab idempotently.
- This make 3 entries into /etc/crontab, but only if certain condition is met.
- This script works with python 3.6.5 and above. Specifically tested with 3.6.5 and 3.7.1.
- This script will not work with Python 2.7.5, default python version found on CentOS 7.
- In my environment, I use pyenv and pipenv to run python version 3.6.5 on CentOS 7. The specific command I run is below:

    ```
    cd ~/env/gp01-3.6.5 && pipenv run sudo ~/.pyenv/shims/python ~/bin/crontab-updater-py36up.py
    ```
- You'd need to be familiar with pyenv and pipenv to use crontab-updater-py36up.py. If you are not, you can use crontab-updater-py27.py instead.
