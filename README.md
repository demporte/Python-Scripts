roject: CPU Utilization Alert Script

Description:

This python script logs the CPU utilization, Network Traffic and Disk Traffic, as well as alerts through 
email if the CPU utilization passes a certain threashhold

Requires a MacOS system with python3, access to cron for automation.

Installation:
Download the script.
Set enviornment variables
edit your crontab to have it execute every hour 00 * * * * /path/to/script.sh



To manually run the script python3 cpu_alert.py

