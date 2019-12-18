import schedule
import time
import site_parser

def job():
    site_parser.parse_and_searching_changes()

schedule.every().day.at("10:00").do(job)
schedule.every().day.at("20:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    