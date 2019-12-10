# -*- coding: utf-8 -*-

def find_class_location_used_number(number_of_class):
    dict_of_all_classes = {
        '1' : 'Мойка, третий этаж, от лестницы налево', 
        '2' : 'Мойка, третий этаж, от лестницы налево',
        '3' : 'Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо',
        '4' : 'ИЭиСТ, третий этаж',
        '5' : 'ИЭиСТ, третий этаж',
        '6' : 'Справа за аркой, что справа от входа в Мойку, который на территории университета',
        '7' : 'ИЭиСТ, третий этаж ИЛИ Мойка, вход со стороны стадиона, второй этаж',
        '8' : 'ИЭиСТ, четвёртый этаж ИЛИ Мойка, вход со стороны стадиона, второй этаж',
        '9' : 'Мойка, вход со стороны стадиона, второй этаж',
        '10' : 'ИЭиСТ, первый этаж',
        '11' : 'ИЭиСТ, первый этаж',
        '12' : 'ИЭиСТ, первый этаж',
        '13' : 'ИЭиСТ, первый этаж',
        '14' : 'Мойка, третий этаж, от лестницы направо, по правую сторону',
        '17' : 'Мойка, второй этаж, налево от охранника, по правую сторону',
        '18' : 'Мойка, второй этаж, налево от охранника, по правую сторону',
        '19' : 'Мойка, второй этаж, налево от охранника, по правую сторону',
        '20' : 'Мойка, второй этаж, налево от охранника, по правую сторону',
        '21' : 'Мойка, второй этаж, налево от охранника, по правую сторону', 
        '26' : 'Мойка, второй этаж, налево от охранника, по левую сторону',
        '28' : 'Мойка, второй этаж, налево от охранника, по левую сторону',
        '33' : 'Мойка, второй этаж, направо от охранника, по левую сторону',
        '34' : 'Мойка, второй этаж, направо от охранника, по левую сторону',
        '35' : 'Мойка, второй этаж, направо от охранника, по правую сторону',
        '36' : 'Мойка, второй этаж, направо от охранника, по правую сторону',
        '39' : 'Мойка, второй этаж, направо от охранника, по правую сторону',
        '40' : 'Мойка, второй этаж, направо от охранника, по левую сторону',
        '42' : 'Мойка, второй этаж, направо от охранника, по левую сторону',
        '43' : 'Мойка, второй этаж, направо от охранника, по правую сторону',
        '44' : 'Мойка, второй этаж, направо от охранника, по правую сторону',
        '45' : 'Мойка, второй этаж, направо от охранника, по правую сторону',
        '46' : 'Мойка, второй этаж, направо от охранника, по левую сторону',
        '54' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца',
        '55' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца',
        '64' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, до конца',
        '71' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону',
        '72' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону',
        '73' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, налево, по левую сторону',
        '78' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца',
        '79' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца',
        '80' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, до конца',
        '81' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, направо, по правую сторону',
        '82' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, по правую сторону',
        '83' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево, направо, по правую сторону',
        '85' : 'Мойка, второй этаж, после угловой лестницы прямо, налево, налево',
        '86' : 'Мойка, второй этаж, после угловой лестницы прямо и налево',
        '87' : 'Мойка, второй этаж, после угловой лестницы прямо',
        '88' : 'Мойка, второй этаж, после угловой лестницы прямо и направо',
        '89' : 'Мойка, второй этаж, после угловой лестницы направо',
        '90' : 'Мойка, второй этаж, после угловой лестницы слева',
        '93' : 'Мойка, первый этаж, после входа направо',
        '94' : 'Мойка, первый этаж, после входа направо',
        '96' : 'Мойка, первый этаж, после входа направо, налево и направо, по левую стороуе',
        '97' : 'Мойка, первый этаж, после входа направо, налево и направо, по левую стороуе',
        '98' : 'Мойка, первый этаж, после входа направо, налево и направо, по левую стороуе',
        '99' : 'Мойка, первый этаж, после входа направо и налево',
        '104' : 'Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо',
        '105' : 'Главный корпус, по лестнице с клеткой на втором этаже вниз, затем налево и прямо',
        '119' : 'Мойка, первый этаж, после входа налево, направо, направо',
        '121' : 'Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '122' : 'Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '123' : 'Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '124' : 'Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '125' : 'Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '126' : 'Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '127' : 'Мойка, первый этаж, после входа налево, направо, налево, по правую сторону',
        '128' : 'Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '129' : 'Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '131' : 'Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '132' : 'Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '135' : 'Мойка, первый этаж, после входа налево, направо, налево, по левую сторону',
        '150' : 'Мойка, справа от спуска к выходу от охранника на втором этаже',
        '223' : 'Мойка, второй этаж, направо от охранника, по левую сторону',
        '233' : 'Мойка, третий этаж, сразу после лестницы',
        '303' : 'Главный корпус, второй этаж, от маленькой лестницы направо',
        '304' : 'Главный корпус, второй этаж, от маленькой лестницы прямо',
        '305' : 'Главный корпус, второй этаж, от маленькой лестницы налево, по левую сторону',
        '306' : 'Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону',
        '307' : 'Главный корпус, второй этаж, от маленькой лестницы налево, по левую сторону',
        '308' : 'Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону',
        '310' : 'Главный корпус, второй этаж, от маленькой лестницы налево, по правую сторону',
        '312' : 'Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, прямо',
        '313' : 'Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне',
        '315' : 'Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне',
        '317' : 'Главный корпус, второй этаж, от лестницы к кафедре анатомии направо, налево, по левой стороне',
        '321' : 'Главный корпус, второй этаж, от главной лестницы налево',
        '322' : 'Главный корпус, второй этаж, от главной лестницы прямо',
        '323' : 'Главный корпус, второй этаж, от главной лестницы направо',
        '401' : 'Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '402' : 'Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '403' : 'Главный корпус, третий этаж, после лестницы направо, направо и прямо',
        '404' : 'Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '405' : 'Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '407' : 'Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '409' : 'Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '410' : 'Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '411' : 'Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '412' : 'Главный корпус, третий этаж, после лестницы направо и направо, по левую сторону',
        '413' : 'Главный корпус, третий этаж, после лестницы направо и направо, по правую сторону',
        '414' : 'Главный корпус, третий этаж, после лестницы направо и прямо',
        '416' : 'Главный корпус, третий этаж, после лестницы налево прямо',
        '418' : 'Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону',
        '419' : 'Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону',
        '421' : 'Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону',
        '422' : 'Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону',
        '423' : 'Главный корпус, третий этаж, после лестницы налево и налево, по левую сторону',
        '426' : 'Главный корпус, третий этаж, после лестницы налево и налево, по правую сторону'
    }   
    try:
        text = dict_of_all_classes[number_of_class]
        return text
    except:
        return 'Такой аудитории я не знаю'

def find_class_location(subject):  
    if 'ауд.' in subject:
        splitted = subject.split(' ')
        for element in splitted:
            if 'ауд.' in element:
                return find_class_location_used_number(element[4:])
    elif 'Зал' in subject:
        if '№2' in subject:
            return 'Манеж, первый этаж'
        elif '№3' in subject:
            return 'Манеж, третий этаж'
        elif '№5' in subject:
            return ''
    elif 'Мойка' in subject:
        if 'к.2' in subject:
            if 'ауд. 7' in subject:
                return 'Мойка, вход со стороны стадиона, второй этаж'
            elif 'ауд. 8' in subject:
                return 'Мойка, вход со стороны стадиона, второй этаж'
            elif 'ауд. 9' in subject:
                return 'Мойка, вход со стороны стадиона, второй этаж'
    elif 'Кафедра' in subject:
        if 'ТиМФОР' in subject:
            return ''
        elif 'ТиМИВС' in subject:
            return ''
        elif 'ПСС' in subject:
            return ''
        elif 'Элективные дисциплины' in subject:
            return ''
        elif 'Педагогики' in subject:
            return 'Мойка, третий этаж, от лестницы направо'
        else:
            return ''
    elif 'Каф.' in subject:
        if 'проф.мед.' in subject:
            return 'Главный корпус, маленькая лестница с выходом к Ленину, второй этаж'
        elif 'анатомии' in subject:
            return 'Главный корпус, по лестнице с клеткой на втором этаже вниз, затем направо'
        elif 'ин.языков' in subject:
            return ''
    elif 'Бассейн' in subject:
        return ''
    elif 'Манеж' in subject:
        return ''
    elif 'Кавголово' in subject:
        return ''
    else:
        return ''
            