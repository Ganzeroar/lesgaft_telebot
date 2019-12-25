import schedule
import time
import site_parser

def job():
    site_parser.parse_and_searching_changes()

# -2 от Мск из-за неизменяемой таймзоры schedule 
schedule.every().day.at("08:00").do(job)
schedule.every().day.at("18:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    