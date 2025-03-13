from django.core.management.base import BaseCommand
import threading
import schedule
import time
from website.services import fetch_and_save_articles

class Command(BaseCommand):
    help = 'Fetch positive news articles twice a day'

    def handle(self, *args, **kwargs):
        def start_scheduler():
            # schedule.every(1).minutes.do(fetch_and_save_articles) # test it by setting it to current time
            schedule.every().day.at("09:00").do(fetch_and_save_articles)
            schedule.every().day.at("18:00").do(fetch_and_save_articles)
            print("Scheduler started...")

            while True:
                schedule.run_pending()
                time.sleep(1)

        # Start the scheduler in a separate thread
        scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
        scheduler_thread.start()

        # Keep the management command running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping scheduler...")

