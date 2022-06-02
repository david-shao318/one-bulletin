from apscheduler.schedulers.blocking import BlockingScheduler
from one_bulletin.accessfeeds import get_all_new_feeds

sched = BlockingScheduler()
sched.add_job(get_all_new_feeds, 'cron', minutes=2)
sched.start()
