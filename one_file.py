# 4. Все таблицы сочетаемости в один файл - перевод всех существительных на английский и поиск прилагательных

import os
import sys
import translations.YandexAPI as Dictionary
from functions import write_file


def make_one_file(path=''):
    result = all_bigrams_one_table(path)
    write_file('all', 'languages', result, '4_translated', path, 'csv')


# Главная функция всего блока
def all_bigrams_one_table(path=''):
    all_bigrams = {}
    for adjective in os.listdir(path + 'result\\3_ready\\'):
        lang = adjective[0:3]
        adj = adjective[4:-4]
        dictionary = Dictionary.YandexApi(
            lang,
            'eng',
            'trnsl.1.1.20170424T150123Z.ca89cfc1fa375d15.b3a867406943f8f73026d936eb06895f1e645495'
        )
        with open(path + 'result\\3_ready\\' + adjective, 'r', encoding='utf-8') as f:
            bigrams_list = f.readlines()

        for bigram in bigrams_list:
            bigram = bigram.rstrip()
            bigram = bigram.lower()
            adjective_bigram, noun = bigram.split(' ')
            if lang != 'eng':
                noun = dictionary.find_translation(bigram)[0]
            words = []
            if noun not in all_bigrams:
                all_bigrams[noun] = words
            all_bigrams[noun].append(adj)
    all_bigrams = make_mas(all_bigrams, path)
    return all_bigrams


# Функция делает масив, более удобный при записи в файл csv
def make_mas(nouns_table, path=''):
    final_table = []
    for noun in nouns_table:
        noun_line = noun + ';'
        for adjective in os.listdir(path + 'result\\3_ready\\'):
            if adjective[4:-4] in nouns_table[noun]:
                noun_line += adjective[4:-4]
            noun_line += ';'
        final_table.append(noun_line)
    return final_table


if __name__ == '__main__':
    # Задайте язык, слово, его кириллический эквивалент(для русского)
    # и (опционально) путь, по которому расположены файлы биграмм
    if len(sys.argv) > 1:
        path_name = sys.argv[1] + '\\'
    else:
        path_name = os.getcwd()
        path_name = path_name[0:path_name.rfind('\\')] + '\\'

    result_table = all_bigrams_one_table(path_name)
    write_file('all', 'languages', result_table, '4_translated', path_name, 'csv')
