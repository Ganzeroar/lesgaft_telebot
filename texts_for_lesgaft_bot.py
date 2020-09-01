# -*- coding: utf-8 -*-

greeting_text = """
Отправь мне полный номер своей группы, чтобы получать актуальное расписание и 
узнавать, где следующая пара, всего в одно нажатие кнопки.

Пример группы: 111

Так же я могу сказать, где находится нужная тебе аудитория, для этого напиши 
мне: «где (№ аудитории)».

Пример: где 233

Вопросы и предложения пиши сюда:
Вк https://vk.com/ganzeroar
Почта ganzeroar@gmail.com

Если вы вдруг ошиблись в номере группы или сменили её, просто отправьте 
правильный номер ещё раз.
"""

group_saved = """
Теперь можно узнавать актуальное расписание с помощью одной кнопки.

Если вы вдруг ошиблись в номере группы или сменили её, просто отправьте 
правильный номер ещё раз.
"""

error = """Упс! Что-то сломалось! 😓

Ошибка будет исправлена в ближайшее время, но ты можешь помочь и ускорить 
процесс - отправь мне в Вк скриншот с сообщением об ошибке 
https://vk.com/ganzeroar или на почту ganzeroar@gmail.com

Заранее спасибо!"""
        
invalid_text = """
Я тебя не понял!

Воспользуйся специальными кнопками с командами или отправь 
один из этих вопросов:
Какие завтра пары?
Где пара?
Где 223

Что бы сменить группу просто напиши 3 цифры своей группы, например "321"
""" 

mystical_error_text = """
Если ты видишь это сообщение, значит ты - тот самый редчайший пользователь, 
который каким-то необъяснимым образом меня сломал. Пожалуйста, свяжись с моим 
создателем в телеграме ( @ganzeroar) или вк, сообщи ему об этом. Тем самым ты 
сделаешь меня чуточку лучше и приблизишь момент нахождения и исправлния этой 
магической ошибки. Заранее спасибо =)
"""

havent_way_to_place = "Упс, у меня ещё нет местоположения этого места. Пожалуйста, не пожалей пары минут и напиши прямо сюда где оно находится, что бы я со временем добавил его к себе в базу."

timetable_lovs_1 = "ФЛОВС, ФИОСТ, Институт менеджмента и социальных технологий"
timetable_lovs_2 = "ФЛОВС, ФИОСТ, Институт менеджмента и социальных технологий"
timetable_lovs_3 = "ФЛОВС, ФИОСТ"
timetable_lovs_4 = "ФЛОВС"
timetable_zovs_1 = "ФЗОВС, Факультет единоборств и НВС, Физкультурное образование, ФИОСТ, Институт здоровья и реабилитологии, Институт АФК, Институт менеджмента и социальных технологий"
timetable_zovs_2 = "ФЗОВС, Факультет единоборств и НВС, ФИОСТ, Институт здоровья и реабилитологии, Институт АФК, Институт менеджмента и социальных технологий"
timetable_zovs_3 = "ФЗОВС, Факультет единоборств и НВС, ФИОСТ, Институт здоровья и реабилитологии, ППО, БЖД, Институт АФК, Институт менеджмента и социальных технологий"
timetable_zovs_4 = "ФЗОВС, Факультет единоборств и НВС, ФИОСТ, Институт здоровья и реабилитологии, Институт АФК, Институт менеджмента и социальных технологий"
timetable_imst = "Институт менеджмента и социальных технологий"
timetable_mag = "МАГИСТРАТУРА. Физическая культура, Психолого-педагогическое образование, Спорт"
timetable_mag_afk = "МАГИСТРАТУРА. Физическая культура для лиц с отклонениями в состоянии здоровья (АФК)"
timetable_mag_tour = "МАГИСТРАТУРА. Туризм, Менеджмент, Журналистика, ГМУ"

timetables_names = [timetable_lovs_1, timetable_lovs_2, timetable_lovs_3, 
    timetable_lovs_4, timetable_zovs_1, timetable_zovs_2, timetable_zovs_3, 
    timetable_zovs_4, timetable_imst, timetable_mag, timetable_mag_afk, timetable_mag_tour]


new_study_year = '''Друзья, прошлое сообщение было тестовым, необходимый этап восстановления работаспособности бота 😁

Бот работает, спасибо за активность всем ночным пользователям! 😘

Активные функции Бота:

(Запрос - отправка сообщения с ключевой фразой.
Кнопка - нажатие на кнопку меню.)

⃣ Запрос "*номер группы*" изменит расписание для выбранной группы. Пример: 119

⃣ Кнопка "Расписание сегодня" покажет сегодняшнее расписание.
🔀 Альтернативный вариант: Запрос "Какие сегодня пары?"

⃣ Кнопка "Расписание на завтра" покажет расписание на следующий день.
🔀 Альтернативный вариант: Запрос "Какие завтра пары?"

⃣ Запрос "Вторник/пятница/*любой день недели*" покажет расписание для выбранного дня. Пример: Четверг

⃣ Запрос "Где *номер аудитории*" поможет найти нужную аудиторию. Пример: Где 223

⃣ Запрос и кнопка "Где пара?" покажет ближайшую по времени пару и местонахождение нужной аудитории.

**Запрос и кнопка "Где пара?" - тестовая функция, если возникнет ошибка - напиши мне Ganzeroar@gmail.com

На данный момент поддерживается расписание только для бакалавриата, расписание магистратуры и ИМиСТ в процессе разработки 😇

⚠Не забудьте изменить номер старой группы на новый! Пример: Группа 219

Всем хорошего дня 🌟'''