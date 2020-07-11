
# A file for running cron job specifically
from controller import cron

print('Start a cron job.')
cron.job()
print('End the cron job.')