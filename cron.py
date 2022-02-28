import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'crontab'])

from crontab import CronTab

cron = CronTab(user='azureuser')
job = cron.new(command='nyt.py')
job.minute.every(1)

cron.write()