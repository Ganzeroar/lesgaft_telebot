import schedule
import time
import site_parser

schedule.every().day.at("10:00").do(site_parser.parse_and_searching_changes())
schedule.every().day.at("20:00").do(site_parser.parse_and_searching_changes())

while True:
    schedule.run_pending()
    time.sleep(1)
    