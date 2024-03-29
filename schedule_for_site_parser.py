import schedule
import time

import site_parser
import main


def job():
    try:
        text = site_parser.run_undergraduate_parser()
        if bool(text):
            raise
        main.send_custom_message_to_user(
            206171081, 'Парсинг прошёл успешно')
    except Exception as exception:
        main.send_custom_message_to_user(
            206171081, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')
        main.send_custom_message_to_user(
            1035761325, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')
        main.send_custom_message_to_user(
            1197606586, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')
        main.send_custom_message_to_user(
            950650249, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')


def final_job():
    try:
        text = site_parser.run_undergraduate_parser()
        if bool(text):
            raise
        main.send_custom_message_to_user(
            206171081, 'Парсинг прошёл успешно')
        main.send_custom_message_to_user(
            5290593854, 'Парсинг прошёл успешно')
    except Exception as exception:
        main.send_custom_message_to_user(
            206171081, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')
        main.send_custom_message_to_user(
            1035761325, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')
        main.send_custom_message_to_user(
            1197606586, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')
        main.send_custom_message_to_user(
            950650249, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')
        main.send_custom_message_to_user(
            5290593854, f'ЭКСЕЛЬ ПАРСЕР не проходит: {exception}')


schedule.every().day.at("11:00").do(job)
schedule.every().day.at("12:00").do(job)
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("14:00").do(job)
schedule.every().day.at("15:00").do(final_job)

while True:
    schedule.run_pending()
    time.sleep(1)
