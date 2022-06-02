import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'project_one_bulletin.settings'
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from one_bulletin.management.commands.accessfeeds import Command as AccessFeedsCommand

sched = BlockingScheduler()


def timed_feed_access():
    cmd = AccessFeedsCommand()
    cmd.handle()


sched.add_job(timed_feed_access, 'interval', id='access_feeds_2_min', minutes=2)

sched.start()
