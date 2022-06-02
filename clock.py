import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'project_one_bulletin.settings'
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
from one_bulletin.management.commands.accessfeeds import Command as AccessFeedsCommand

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_feed_access():
    call_command(AccessFeedsCommand())


sched.start()
