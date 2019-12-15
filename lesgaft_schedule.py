import schedule
import time
import site_parser

def job():
    site_parser.parse_and_searching_changes()

schedule.every(2).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    