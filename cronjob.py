
# A file for running cron job specifically
from controller import cron

print('Start a cron job.')
cron.job('opinion_leaders')
print('Finish crawling opinion leaders.')
cron.job('company_comments')
print('Finish crawling company comments.')