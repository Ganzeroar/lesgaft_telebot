month_to_skip = ['08', '09', '10', '11', '12', '01', '02', '03', '05', '06', '07']
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
    'ин.яз. (2)',
    'тимобвс лыжный спорт (2)',
    'тимобвс гимнастика (2)',

]

day_and_month_to_parse = [
    '02.04.',
    '09.04.',
    '16.04.',
    '23.04.',
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
        'group_specialization_row': 5,
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
        'specialization' : [
            'Художественная гимнастика\nХудожественная гимнастика\n(антидопинг)',
            'Художественная гимнастика',
            'Танц. спорт\nСпорт. аэробика',
            'Спорт. акроб.\nЭст.гимн.\nАкроб. р-н-рл\nСпорт. гимн.',
            'Футбол\nТеннис',
            'Футбол\nФутбол (антидопинг)\nГандбол',
            'Баскетбол',
            'Наст. теннис\nВолейбол\nВолейбол (антидопинг)',
            'Плавание I',
            'Плавание II',
            'Легк. атл.',
            'Легк. атл. (менеджмент ФКиС)\nЛегк. атл. (ССИ)',
            'Велоспорт\nГребной спорт\nПарусный спорт\nТриатлон\nАвт.спорт',
        ],
    },
    'lovs_2' : {
        'group_row': 4, 
        'group_specialization_row': 5,
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
        'specialization' : [
            'Худ. гимн.\nХуд. гимн. (антидопинг)',
            'Худ. гимн.',
            'Танц. спорт\nСпорт. аэробика\nСпорт. аэробика (менеджмент)',
            'Спорт. акроб\nЭстет. гимн\nАкроб. рок-н-ролл\nСпорт. гимн\nСпорт. акроб (менеджмент)\nЭстет. гимн\n(менеджмент)\nАкроб. рок-н-ролл\n(менеджмент)\nСпорт. гимн (ССИ)',
            'Плавание I',
            'Плавание II',
            'Плавание III\nПлавание (ФОД)\nПлавание (менеджмент)\nПлавание (антидопинг)\nПлавание (ССИ)',
            'Баскетбол\nГандбол\nГандбол (менеджмент)\nГандбол (антидопинг)\nБаскетбол (антидопинг)',
            'Теннис\nНаст.теннис\nВолейбол\nТеннис (менеджмент)\nВолейбол (менеджмент)\nЛегк.атл. (менеджмент)\nВолейбол (антидопинг)\nЛегк.атл. (антидопинг)\nВолейбол (ССИ)\nЛегк.атл. (ССИ)',
            'Легкая атлетика',
            'Футбол\nФутбол (менеджмент)\nФутбол (антидопинг)',
            'Велоспорт\nГребной спорт\nПарусн. спорт\nВодно-мат. спорт\nАкад.гребля\n(антидопинг)\nПарусн. спорт (менеджмент)',
        ],
    },
    'lovs_3' : {
        'group_row': 4,
        'group_specialization_row': 5,
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
        'specialization' : [
            'Худ. гимнастика',
            'Танц. спорт, Спорт. гимн., Акроб. рок-н-ролл',
            'Эстет. гимн., Спорт. аэробика., Спорт. акроб.',
            'Футбол I',
            'Футбол II',
            'Баскетбол\nТеннис',
            'Гандбол\nВолейбол\nНаст. теннис',
            'Легкая атлетика',
            'Плавание I',
            'Плавание II\nФОД',
            'Велоспорт\nАвтоспорт\nПарусный спорт\nГребной спорт',
            'Направленность (профиль):\nМенеджмент ФКиС\nФутбол, волейбол, л/а, плавание (менеджмент ФКиС)',
            'Направленность (профиль):\nССиИ\nПлавание (ССиИ)',
            'Спорт. аэробика, л/а, теннис, плавание, футбол (антидопинг)',
        ],

    },
    'lovs_4' : {
        'group_row': 4,
        'group_specialization_row': 5,
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
        'specialization' : [
            'Худ. гимн.',
            'Танцев. спорт\nСпорт. гимн.\nАкроб. рок-н-ролл\nСпорт. аэробика',
            'Спорт. акроб.\nЭст. гимн.\nХуд. гимн.',
            'Плавание I',
            'Плавание II',
            'Баскетбол\nГандбол',
            'Теннис\nНаст. теннис\nВолейбол',
            'Легк. атл.',
            'Футбол I',
            'Антидопинговое обеспечение в спорте\nТанц.спорт\nСпорт.акроб.\nВодные виды спорта\nАкадем. гребля\nГандбол\nВолейбол\nЛегк. атл.\nПлавание',
            'Менеджмент ФКиС\nХуд. Гимн\nВодные виды спорта\nВодное поло\nБаскетбол',
            'Футбол II',
            'Велоспорт \nГребной спорт\nПарусн. спорт\nВодно-моторный спорт',
        ],
    },
    'zovs_1' : {
        'group_row': 4,
        'group_specialization_row': 5,
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
        'specialization' : [
            'Атлетизм\nТхэквондо\nТхэквондо (антидопинг)',
            'Борьба',
            'Бокс\nБокс (антидопинг)\nКикбоксинг',
            'Бильярд, Дартс, Регби, Шахматы, Шашки, Спорт.ориент., Спорт.туризм, Фехтование',
            'Полиатлон\nПолиатлон (фод)\nПолиатлон (антидопинг)\nКомпьютерный спорт ',
            'Физкультурное образование',
            'Психология спорта',
            'Хоккей',
            'Фигурное катание',
            'Фигурное катание\nФигурное катание (антидопинг)',
            'ТиМ ОБВС: лыжный спорт',
            'Биатлон, Биатлон (антидопинг), Скалолазание, Керлинг, Керлинг (антидопинг), Конькобежый спорт',
        ],
    },
    'zovs_2' : {
        'group_row': 4,
        'group_specialization_row': 5,
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
        'specialization' : [
            'Пауэрлифтинг\nГиревой спорт\nБодибилдинг\nТяжелая атлетика\nФехтование\nФехтование (антидопинг)',
            'Борьба\nДзюдо\nСамбо\nГреко-римская\nСамбо (антидопинг)\nДзюдо (менеджмент)\nДзюдо (антидопинг)',
            'Тхэквондо\nТхэквондо (антидопинг)\nКикбоксинг\nБокс',
            'Дартс\nШахматы\nШашки\nБильярд\nГород.спорт\nРегби\nСпорт.ориент.\nКиберспорт\nПолиатлон\nПолиатлон (ФОД)\nСпорт.ориент (антидопинг)\nПолиатлон (менеджмент)\nПолиатлон (антидопинг)',
            'Направленность (профиль):\nФизкультурное образование',
            'Направленность (профиль):\nПсихология спорта',
            'Хоккей\nХоккей (антидопинг)\nХоккей (менеджмент)',
            'Хоккей',
            'Фигурное катание на коньках\nФигурное катание на коньках (антидопинг)',
            'Горнолыжный спорт\nЛыжные гонки\nПрыжки на лыжах с трамплина\nЛыжный спорт (антидопинг)\nЛыжный спорт (менеджмент)',
            'Биатлон\nКерлинг\nКонькобежный спорт\nБиатлон (антидопинг)\nБиатлон (ССИ)',
            '',
            '',
        ],
    },
    'zovs_3' : {
        'group_row': 4,
        'group_specialization_row': 5,
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
        'specialization' : [
            'Атлетизм: Пауэрлифтинг, Гиревой спорт, Бодибилдинг, Тяжелая атлетика, Бокс',
            'Борьба\nДзюдо',
            'Самбо\nГреко-римская борьба\nТхэквондо',
            'Кикбоксинг',
            'Физкультурное образование',
            'Фехтование\nКомп. спорт',
            'Дартс, Регби, Бильярд, Шахматы, Городошный спорт, Спорт. туризм, Спорт. ориент.',
            'Хоккей',
            'Полиатлон (ФОД)',
            'Коньк. спорт\nФигурн. кат.',
            'Фигурн. кат.',
            'Горнолыжный спорт, Лыжные гонки, Сноубординг, Прыжки на лыжах с трамплина, Фристайл',
            'Биатлон\nСкалолазание\nКерлинг',
            'Направленность (профиль):\nМенеджмент ФКиС\nМенеджмент (тхэквондо, дзюдо, кикбиксинг, скалолазание, керлинг, полиатлон, хоккей, дартс, фехтование)',
            'Направленность (профиль):\nССиИ\nССиИ (тхэквондо, дартс)',
            'Антидопинг\n(комп. Спорт., тхэквондо, кикбоксинг, дартс, полиатлон, биатлон, фигурн. кат., коньк. спорт, пауэрлифтинг\nгиревой спорт)',
        ],
    },
    'zovs_4' : {
        'group_row': 4,
        'group_specialization_row': 5,
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
        'specialization' : [
            'Самбо\nАтлетизм',
            'Борьба\nДзюдо\nФехтование',
            'Киберспорт\nТхэквондо',
            'Бокс\nКикбоксинг',
            'Дартс\nРегби\nБильярд\nШахматы\nСпорт. туризм\nСпорт. ориент.',
            'Хоккей',
            'ФОД\nВодные виды спорта',
            'ФОД Полиатлон\nХоккей',
            'Коньк. спорт\nФигурн. кат.',
            'Лыжный спорт',
            'Биатлон\nКерлинг',
            'Антидопинговое обеспечение в спорте\nТяж.атл.\nБодибилдинг\nДзюдо\nКикбоксинг\nБокс\nСпорт.ориент.\nХоккей\nЛыжный спорт\nПолиатлон',
            'Менеджмент\nГреко - римская борьба\nЛыжный спорт\nСпорт.туризм\nХоккей\nГорн. Спорт\nКерлинг\nБиатлон',
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