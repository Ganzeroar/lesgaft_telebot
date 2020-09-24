import schedule
import time

import site_parser
import main

def job():
    try:
        site_parser.run_undergraduate_parser()
    except Exception as exception:
        main.send_custom_message_to_user(206171081, f'ЭКСЕЛЬ ПАРСЕР УМЕР потому что {exception}')
        print(exception)

    #site_parser.run_all_parsers()

# -2 от Мск из-за неизменяемой таймзоны schedule 
schedule.every().day.at("08:00").do(job)
schedule.every().day.at("18:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    