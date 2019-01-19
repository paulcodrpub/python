# Updated: 2019.01.18

# Goal
# Scan CentOS 7 and update /etc/crontab accordingly.

# Tested on python versions:
# 2.7.5

# Not compatible with python 3.x and above

# To run
# This script is designed to run with python 2.7.5, default on CentOS 7. 
# So as a normal user with sudo privilege, run below:
# >>> cd; sudo python ~/bin/crontab-updater-py27.py

# Or as root, run following:
# >>> cd; python ~/bin/crontab-updater-py27.py
# Running 'cd;' first ensures you are not using any pipenv environment unintentionally.


import platform
import re
import os
import datetime
import shutil
import filecmp
# import time  # for pausing script, used in testing


osverTarget = 'centos-7'
fileTarget = '/etc/crontab'
now = datetime.datetime.now().strftime('%Y-%m-%d--%H%M')
fileTargetBackup = fileTarget + '-' + now
counterTotal = 0
counterUsed = 0


if 'centos-7' in platform.platform():    
    # platform.platform() return example: 
    # 'Linux-3.10.0-957.1.3.el7.x86_64-x86_64-with-centos-7.6.1810-Core'
    osver = 'centos-7'


# Backup /etc/crontab first
def func_backup_crontab():
    now = datetime.datetime.now().strftime('%Y-%m-%d--%H%M')
    if osver == osverTarget:
        fileTargetBackup = fileTarget + '-' + now
        shutil.copy(fileTarget, fileTargetBackup)


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
    exists = os.path.isfile('/usr/bin/certbot')  # different in crontab-updater-py36up.py
    counterTotal += 1    
    if exists:
        with open(fileTarget, 'r+') as fh:
            text = fh.read()
            if re.search(r'(?m)certbot\ renew', text):
                print('certbot: No change required.')
            else:
                fh.write('\n\n30 2 * * 1 root /bin/date >> /var/log/le-renew.log; /usr/bin/certbot renew --post-hook "/usr/bin/systemctl reload nginx" >> /var/log/le-renew.log  # LetsEncrypt auto renewal')
                print('LetsEncrypt certbot renewal scheduled.')
                counterUsed += 1


def func_counter():
    print """\nOut of possible %s updates to %s, 
total of %s updates were made.""" % (counterTotal, fileTarget, counterUsed)


def func_delete_backup_if_necessary():
    if filecmp.cmp(fileTarget, fileTargetBackup, shallow=False):
        # print(fileTargetBackup)
        # time.sleep(5)   # for testing
        os.remove(fileTargetBackup)
        print """\nFile '%s' remains unchanged, so backup file 
'%s'  (created as script execution started) has been deleted.""" % (fileTarget, fileTargetBackup)
    else:
        print """\nBefore file '%s' was updated, it was backed up to
'%s'.""" % (fileTarget, fileTargetBackup)


func_backup_crontab()
func_strip_end_blank_line()
func_yumupdate()
func_cpuram()
func_certbot()
func_counter()
func_delete_backup_if_necessary()
