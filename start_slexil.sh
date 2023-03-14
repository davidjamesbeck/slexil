#!/bin/bash
#
# Start slexil, if it isn't running.
# Must be run by dbeck.
#

# is slexil already running?
if pgrep gunicorn > /dev/null;then
   echo -e "\nslexil appears to be running already.\n"
   exit 1
fi

# who is trying to run this script?
#if [ "$UID" != "1004" ];then
#   echo -e "\nERROR: You must run this as dbeck.\n"
#   echo -e "If you are root, try\n
#   sudo -H -u dbeck /home/dbeck/start_slexil.sh\n\n"
#   exit 99
#fi

cd ~/github/slexil/tests
#git pull origin master
#cd tests
~/.local/bin/virtualenv --python=/usr/bin/python3 ./py368
source py368/bin/activate
#pip install -r ../requirements.txt
cd ..
nohup gunicorn -w 4 -t 240 webapp4:server

exit 0
