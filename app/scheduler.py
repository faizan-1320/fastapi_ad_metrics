# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

def log_job():
    print(f"[CRON JOB] Ran successfully at {datetime.now()}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # ⏰ Run every 6 hours using interval (or use cron if preferred)
    scheduler.add_job(log_job, trigger='interval', hours=6)

    # Or use cron: every day at 0, 6, 12, 18 hours
    # scheduler.add_job(log_job, trigger=CronTrigger(hour='0,6,12,18'))

    scheduler.start()
