from crontab import CronTab

cron = CronTab(user='azureuser')
job = cron.new(command='nyt.py')
job.minute.every(1)

cron.write()