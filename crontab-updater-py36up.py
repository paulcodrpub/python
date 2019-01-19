# Updated: 2019.01.16

# Goal
# Scan CentOS 7 and update /etc/crontab accordingly.

# Tested on python versions:
# 3.6.5
# 3.7.1

# Not compatible with python 3.5.6 and below.

# To run  * Uses pipenv
# cd ~/env/gp01-3.6.5 && pipenv run sudo ~/.pyenv/shims/python ~/bin/crontab-updater-py36up.py


import platform
import re
from pathlib import Path
import datetime
import filecmp
# import time  # for pausing script, used in testing


osverTarget = 'centos-7'
fileTarget = Path('/etc/crontab')
now = datetime.datetime.now().strftime('%Y-%m-%d--%H%M')
fileTargetBackup = Path(str(fileTarget) + '-' + now)
counterTotal = 0
counterUsed = 0


if 'centos-7' in platform.platform():    
    # platform.platform() return example: 
    # 'Linux-3.10.0-957.1.3.el7.x86_64-x86_64-with-centos-7.6.1810-Core'
    osver = 'centos-7'


# Backup /etc/crontab first
def func_backup_crontab_pathlib():
    # Since Python 3.5, without importing shutil, you can do below: 
    fileTargetBackup.write_text(fileTarget.read_text()) #for text files


def func_strip_end_blank_line():
    with open(fileTarget) as fh1:
        fh1_cleaned = fh1.read().rstrip('\n')

    with open(fileTarget, 'w') as f_output:    
        f_output.write(fh1_cleaned)


def func_yumupdate():
    global counterTotal
    global counterUsed
    counterTotal += 1
    if osver == osverTarget:
        with open(fileTarget, 'r+') as fh:
            text = fh.read()
            if re.search(r'(?m)yumupdate.sh', text):
                print('yumupdate: No change required.')
            else:
                fh.write('\n\n1 11 * * 1,3,5 root /root/bin/yumupdate.sh  # yumupdate-cron')
                print('yumupdate.sh cron job scheduled.')
                counterUsed += 1


def func_cpuram():
    global counterTotal
    global counterUsed
    counterTotal += 1
    if osver == osverTarget:
        with open(fileTarget, 'r+') as fh:
            text = fh.read()
            if re.search(r'(?m)cpuram-logger', text):
                print('cpuram: No change required.')
            else:
                fh.write('\n\n0,10,20,30,40,50 * * * * root /root/bin/cpuram-logger.sh  # cpu & ram usage logger')
                print('cpuram-logger.sh cron job scheduled.')
                counterUsed += 1


def func_certbot():
    global counterTotal
    global counterUsed
    certfile = Path("/usr/bin/certbot") # different in crontab-updater-py27.py
    counterTotal += 1
    if certfile.is_file():
        with open(fileTarget, 'r+') as fh:
            text = fh.read()
            if re.search(r'(?m)certbot\ renew', text):
                print('certbot: No change required.')
            else:
                fh.write('\n\n30 2 * * 1 root /bin/date >> /var/log/le-renew.log; /usr/bin/certbot renew --post-hook "/usr/bin/systemctl reload nginx" >> /var/log/le-renew.log  # LetsEncrypt auto renewal')
                print('LetsEncrypt certbot renewal scheduled.')
                counterUsed += 1


def func_counter():
    print(f"""\nOut of possible {counterTotal} updates to {fileTarget}, 
total of {counterUsed} updates were made.""")


def func_delete_backup_if_necessary():
    if filecmp.cmp(fileTarget, fileTargetBackup, shallow=False):
        # print(fileTargetBackup)
        # time.sleep(5)   # for testing
        fileTargetBackup.unlink()
        print(f"""\nFile '{fileTarget}' remains unchanged, so backup file 
'{fileTargetBackup}' (created as script execution started) has been deleted.""")
    else:
        print(f"""\nBefore file '{fileTarget}' was updated, it was backed up to
'{fileTargetBackup}'.""")


func_backup_crontab_pathlib()
func_strip_end_blank_line()
func_yumupdate()
func_cpuram()
func_certbot()
func_counter()
func_delete_backup_if_necessary()
