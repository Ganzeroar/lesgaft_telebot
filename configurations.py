month_to_skip = ['08', '09', '10', '11', '12', '01', '02', '05', '06', '07']
day_to_parse = ['02']
words_to_skip = [
    'тимивс',
    'псс',
    'тст',
    'шапка',
    'лыжи',
    'ссылки',
    'список школ',
    'ссылки л.атл',
    'тимивс,тст,псс',
    'ссылки афк',
    'тимобвс лыжный спорт',
    'тимобвс гимнастика',
    'ин.яз.',
    'ссылки л.атл, гимн',
    'ссылки ин. яз.',
    'тимивс,элект.дисц.,псс',

]

day_and_month_to_parse = [
    '02.04.',
    '09.04.',
]

non_standart_group = [
    'фод, водные виды спорта',
    'плавание ii',
    'антидопинговое обеспечение в спорте, танц.спорт, спорт.акроб., водные виды спорта, академ. гребля,гандбол,волейбол,легк. атл., плавание',
    'самбо, атлетизм',
    'борьба, дзюдо, фехтование',
    'менеджмент фкис, худ. гимн, водные виды спорта, водное поло баскетбол',
    'спорт. аэробика, л/а, теннис, плавание, футбол (антидопинг)',
    'антидопинг (комп. спорт., тхэквондо, кикбоксинг, дартс, полиатлон, биатлон, фигурн. кат., коньк. спорт, пауэрлифтинг, гиревой спорт)'
]

non_standart_group_327 = [
    'направленность (профиль): менеджмент фкис, футбол, волейбол, л/а, плавание (менеджмент фкис)',
    'направленность (профиль): ссии, плавание (ссии)',
    'направленность (профиль): менеджмент фкис, менеджмент (тхэквондо, дзюдо, кикбиксинг, скалолазание, керлинг, полиатлон, хоккей, дартс…',
    'направленность (профиль): ссии, ссии (тхэквондо, дартс)'
]

#подбить константы под каждое расписание
group_constants = {
    'lovs_1' : {
        'group_row': 4, 
        'first_group_column': 4, 
        'first_group_number': 'Группа 101', 
        'last_group_column': 16, 
        'last_group_number': 'Группа 113',
        'date_column': 1,
        'first_date_row': 6,
        'day_column': 2,
        'first_day_row': 6,
        'time_column': 3,
        'first_time_row': 6,
        'group_numbers': [
            'Группа 101',
            'Группа 102',
            'Группа 103',
            'Группа 104',
            'Группа 105',
            'Группа 106',
            'Группа 107',
            'Группа 108',
            'Группа 109',
            'Группа 110',
            'Группа 111',
            'Группа 112',
            'Группа 113',
        ],
    },
    'lovs_2' : {
        'group_row': 4, 
        'first_group_column': 4, 
        'first_group_number': 'Группа 201', 
        'last_group_column': 15, 
        'last_group_number': 'Группа 212',
        'date_column': 1,
        'first_date_row': 6,
        'day_column': 2,
        'first_day_row': 6,
        'time_column': 3,
        'first_time_row': 6,
        'group_numbers': [
            'Группа 201',
            'Группа 202',
            'Группа 203',
            'Группа 204',
            'Группа 205',
            'Группа 206',
            'Группа 207',
            'Группа 208',
            'Группа 209',
            'Группа 210',
            'Группа 211',
            'Группа 212',
        ],
    },
    'lovs_3' : {
        'group_row': 4, 
        'first_group_column': 4, 
        'first_group_number': 'Группа 301', 
        'last_group_column': 16, 
        'last_group_number': 'Группа 328',
        'date_column': 1,
        'first_date_row': 6,
        'day_column': 2,
        'first_day_row': 6,
        'time_column': 3,
        'first_time_row': 6,
        'group_numbers': [
            'Группа 301',
            'Группа 302',
            'Группа 303',
            'Группа 304',
            'Группа 305',
            'Группа 306',
            'Группа 307',
            'Группа 308',
            'Группа 309',
            'Группа 310',
            'Группа 311',
            'Группа 327',
            'Группа 328',
        ],
    },
    'lovs_4' : {
        'group_row': 4, 
        'first_group_column': 4, 
        'first_group_number': 'Группа 401', 
        'last_group_column': 16, 
        'last_group_number': 'Группа 411',
        'date_column': 1,
        'first_date_row': 6,
        'day_column': 2,
        'first_day_row': 6,
        'time_column': 3,
        'first_time_row': 6,
        'group_numbers': [
            'Группа 401',
            'Группа 402',
            'Группа 403',
            'Группа 404',
            'Группа 405',
            'Группа 406',
            'Группа 407',
            'Группа 408',
            'Группа 409',
            'Группа 412',
            'Группа 413',
            'Группа 410',
            'Группа 411',
        ],
    },
    'zovs_1' : {
        'group_row': 4, 
        'first_group_column': 4, 
        'first_group_number': 'Группа 114', 
        'last_group_column': 15, 
        'last_group_number': 'Группа 125',
        'date_column': 1,
        'first_date_row': 6,
        'day_column': 2,
        'first_day_row': 6,
        'time_column': 3,
        'first_time_row': 6,
        'group_numbers': [
            'Группа 114',
            'Группа 115',
            'Группа 116',
            'Группа 117',
            'Группа 118',
            'Группа 119',
            'Группа 120',
            'Группа 121',
            'Группа 122',
            'Группа 123',
            'Группа 124',
            'Группа 125',
        ],
    },
    'zovs_2' : {
        'group_row': 4, 
        'first_group_column': 4, 
        'first_group_number': 'Группа 213', 
        'last_group_column': 14, 
        'last_group_number': 'Группа 223',
        'date_column': 1,
        'first_date_row': 6,
        'day_column': 2,
        'first_day_row': 6,
        'time_column': 3,
        'first_time_row': 6,
        'group_numbers': [
            'Группа 213',
            'Группа 214',
            'Группа 215',
            'Группа 216',
            'Группа 217',
            'Группа 218',
            'Группа 219',
            'Группа 220',
            'Группа 221',
            'Группа 222',
            'Группа 223',
        ],
    },
    'zovs_3' : {
        'group_row': 4, 
        'first_group_column': 4, 
        'first_group_number': 'Группа 312', 
        'last_group_column': 18, 
        'last_group_number': 'Группа 328',
        'merged_group': 'Группа 327',
        'date_column': 1,
        'first_date_row': 6,
        'day_column': 2,
        'first_day_row': 6,
        'time_column': 3,
        'first_time_row': 6,
        'group_numbers': [
            'Группа 312',
            'Группа 313',
            'Группа 314',
            'Группа 315',
            'Группа 316',
            'Группа 317',
            'Группа 318',
            'Группа 319',
            'Группа 320',
            'Группа 321',
            'Группа 322',
            'Группа 323',
            'Группа 324',
            'Группа 327',
            'Группа 327',
            'Группа 328',
        ],
    },
    'zovs_4' : {
        'group_row': 4, 
        'first_group_column': 4, 
        'first_group_number': 'Группа 412', 
        'last_group_column': 16, 
        'last_group_number': 'Группа 425',
        'date_column': 1,
        'first_date_row': 6,
        'day_column': 2,
        'first_day_row': 6,
        'time_column': 3,
        'first_time_row': 6,
        'group_numbers': [
            'Группа 412',
            'Группа 413',
            'Группа 414',
            'Группа 415',
            'Группа 416',
            'Группа 417',
            'Группа 405',
            'Группа 418',
            'Группа 419',
            'Группа 420',
            'Группа 421',
            'Группа 424',
            'Группа 425',
        ],
    }
}

string_for_stop_vertical_parsing = ['Начальник УМУ Паульс А.А.', 'Начальник УМУ Овсюк Т.М.']

days_of_week = ['Пн.','Вт.','Ср.','Чт.','Пт.','Сб.']
lesson_start_times = ['9:45', '11:30', '13:30', '15:15', '17:00', '18:40']

#type 1 - 4 lines
#type 2 - 3 lines
#type 3 - 2 lines 
existing_locations = [
    '1 ИМиСТ',
    '2 ИМиСТ',
    '3 ИМиСТ',
    '4 ИМиСТ',
    '5 ИМиСТ',
    '10 ИМиСТ',
    '11 ИМиСТ',
    '12 ИМиСТ',
    '13 ИМиСТ',
    '14',
    '19',
    '20',
    '21',
    '35',
    '39',
    '40',
    '86',
    '139',
    '150',
    '223',
    '233',
    '304',
    '312',
    '315',
    '409',
    '411',
    '412',
    '413',
    '419',
    '421',
    '422',
    '423',
    '426',
    'УТЦ "КАВГОЛОВО"',
    'Зал № 2',
    'Зал № 3',
    'Кафедра',
    'Манеж',
    'Кафедра плавания',
    'Кафедра педагогики',
    'ауд. 86',
]
existing_subjects = [
    'Профилактика негативных социальных явлений средствами ФКиС',
    'Физиология человека',
    'Биомеханика двигательной деятельности',
    'Педагогика ФКиС',
    'ТиМ ФК',
    'Экономика ФКиС',
    'Философия',
    'Социология ФК',
    'Безопасность жизнедеятельности',
    'Информационные технологии в ФКиС',
    'История ФКиС',
    'Правовые основы профессиональной деятельности',
    'Спортивная метрология',
    'Профессиональная этика',
    'ТиМ ОБВС: лыжный спорт',
    'Элективные дисциплины по ФКиС',
    'ТиМ ОБВС: Плавание',
    'ТиМ ИВС',
    'ТиМ ОБВС: Волейбол',
    'Профилактика негативных социальных явлений средствами ФКиС',
    'Иностранный язык',
    'Русский язык и культура речи',
    'ТиМ ОБВС: Гимнастика',
    'Анатомия человека',
    '',
    '',
    '',

]
existing_type_of_subject_type_1 = ['Семинар', 'Лекция']
existing_teachers = [
'Большова Е.В.',
'Щедрина Ю.А.',
'Захаров Ф.Е.',
'Макаров А.А.',
'Сафронова М.А.',
'Гомзякова И.П.',
'Латышева Н.Е.',
'Дранюк О.И.',
'Андросова Г.А.',
'Медведева О.А.',
'Догонова Н.А.',
'Утишева Е.В.',
'Оганян К.К.',
'Белогородцева Э.И.',
'Селитренникова Т.А.',
'Предовская М.М.',
'Селивёрстова В.В.',
'Кармаев Н.А.',
'Мурзина А.С.',
'Дьяченко Н.А.',
'Димура И.Н.',
'Цикунова Н.С.',
'Калашникова Е.В.',
'Сухляева А.В.',
'Кротова Н.Ю.',
'Самсонов М.А.',
'Гуркин Я.А.',
'Бородин Д.А.',
'Рыбакова О.Б.',
'Ципин Л.Л.',
'Худякова А.С.',
'Казаринова Л.В.',
'Руденко М.А.',
'Курашова Е.А.',
'Кудрявцева З.Н.',
'Говорков Л.П.',
'Денисенко А.Н.',
'Пудло П.М.',
'Щеглов И.М.',
'Ермаков Д.А.',
'Аксенова Н.Н.',
'Косьмина Е.А.',
'Голокова М.С.',
'Комева Е.Ю.',
'Серов С.В.',
'Биленко А.Г.',
'Буренко В.О.',
'Назимкова В.С.',
'Чудаев М.Е.',
'Живодёров В.А.',
'Супрун А.А.',
'Бердышева Н.Ю.',
'Смирнов А.А.',
'Осипова Е.В.',
'Суровцева О.Н.',
'Бордовский П.Г.',
'',
'',
]

existing_practice = [
    'Учебная практика'
]

strings_to_skip_while_no_format = [
    'УП',
    'ТиМ ОБВС: Гимнастика',
    'Иностранный язык',
    'ТиМ ИВС',
    'Элективные дисциплины по ФКиС',
    'Анатомия человека',
    '',
    '',

]

existing_location_type_3 = []
#existing_subjects_type_3 = []
#existing_teachers_type_1 = {
#    ''
#}
existing_location_type_2 = []
#existing_subjects_type_2 = []