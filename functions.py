# Файл со служебными функциями

import os
import translations.YandexAPI as Dictionary


# Проверяет, имеют ли массивы общие элементы
def check_arrays_for_commons(m1, m2):
    for element in m1:
        if element in m2:
            return element
    return False


# Делает словарь
def make_dict(lang, languages, bigrams):
    dictionaries = {}
    for foreign_language in languages:
        if foreign_language != lang:
            one_dict = {}
            dictionary = Dictionary.YandexApi(
                lang,
                foreign_language,
                'trnsl.1.1.20170424T150123Z.ca89cfc1fa375d15.b3a867406943f8f73026d936eb06895f1e645495'
            )
            for line in bigrams:
                line = line.rstrip()
                adj, noun = line.split(' ')
                one_dict[noun] = dictionary.find_translation(line)
            dictionaries[foreign_language] = one_dict
    return dictionaries


# функция поиска всех языков
def all_languages(path=''):
    languages = []
    for element in os.listdir(path + 'result\\3_ready\\'):
        if element[0:3] not in languages:
            languages.append(element[0:3])
    return languages


# Общая функция записи
def write_file(lang, name, file, folder='0', path='', exp='txt'):
    if not os.path.exists(path + 'result\\' + folder + '\\'):
        os.makedirs(path + 'result\\' + folder + '\\')
    with open(path + 'result\\' + folder + '\\' + lang + '_' + name + '.' + exp, 'w', encoding='utf-8') as d:
        for line in file:
            d.write(line + '\n')
