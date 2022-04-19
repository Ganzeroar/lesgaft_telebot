import schedule
import time

import site_parser
import main


def job():
    try:
        site_parser.run_undergraduate_parser()
        main.send_custom_message_to_user(
            206171081, 'Парсиг прошёл успешно')
    except Exception as exception:
        main.send_custom_message_to_user(
            206171081, f'ЭКСЕЛЬ ПАРСЕР УМЕР потому что {exception}')
        main.send_custom_message_to_user(
            1035761325, f'ЭКСЕЛЬ ПАРСЕР УМЕР потому что {exception}')
        main.send_custom_message_to_user(
            1197606586, f'ЭКСЕЛЬ ПАРСЕР УМЕР потому что {exception}')

def final_job():
    try:
        site_parser.run_undergraduate_parser()
        main.send_custom_message_to_user(
            206171081, 'Парсиг прошёл успешно')
    except Exception as exception:
        main.send_custom_message_to_user(
            206171081, f'ЭКСЕЛЬ ПАРСЕР УМЕР потому что {exception}')
        main.send_custom_message_to_user(
            1035761325, f'ЭКСЕЛЬ ПАРСЕР УМЕР потому что {exception}')
        main.send_custom_message_to_user(
            1197606586, f'ЭКСЕЛЬ ПАРСЕР УМЕР потому что {exception}')
        main.send_custom_message_to_user(
            5290593854, f'ЭКСЕЛЬ ПАРСЕР не проходит потому что {exception}')

schedule.every().day.at("11:00").do(job)
schedule.every().day.at("12:00").do(job)
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("14:00").do(job)
schedule.every().day.at("15:00").do(final_job)

while True:
    schedule.run_pending()
    time.sleep(1)
