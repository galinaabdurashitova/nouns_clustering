# 4. Поиск существительных из биграмм в биграммах с другими прилагательными (перевод)
# Данный блок не используется в представленной работе

import os
import sys
from functions import write_file, all_languages, make_dict


def translate_bigrams(lang, name, path=''):
    result_table, not_translated_nouns = translate(lang, name, all_languages(path), path)
    write_file(lang, name, not_translated_nouns, 'not_translated', path)
    write_file(lang, name, result_table, '4_translated', path, 'csv')


# Главная функция всего блока
def translate(lang, name, languages, path=''):
    with open(path + 'result\\3_ready\\' + lang + '_' + name + '.txt', 'r', encoding='utf-8') as f:
        bigrams_list = f.readlines()

    dictionaries = make_dict(lang, languages, bigrams_list)

    result_line = {}
    i = 1
    for element in os.listdir(path + 'result\\3_ready\\'):  # Просматриваю все остальные слова ряда
        if name not in element:
            i += 1
            main_foreign_word = element[4:-4]
            main_foreign_lang = element[0:3]

            # Все существительные, найденные в биграммах для заданного прилагательного
            foreign_nouns = make_list_foreign_nouns(element, path)

            if main_foreign_lang != lang:
                # Функция, которая добавляет в result_line столбик с новым словом
                result_line = main_file_searching_translations(main_foreign_word, dictionaries[main_foreign_lang],
                                                               bigrams_list, foreign_nouns, result_line, i)
            else:
                result_line = main_file_same_language(main_foreign_word, bigrams_list, foreign_nouns, result_line, i)

    # Функция делает масив, более удобный при записи в файл csv
    result_line, not_translated_list = make_mas(lang, result_line, path)

    return result_line, not_translated_list


# Все существительные, найденные в биграммах для заданного прилагательного
def make_list_foreign_nouns(filename, path=''):
    nouns = []
    with open(path + 'result\\3_ready\\' + filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            adj, noun = line.split(' ')
            nouns.append(noun)
    return nouns


# 2 функции, которые добавляют в result_line столбик с новым словом (для разных языков и одного языка)
def main_file_searching_translations(foreign_word, dictionary, bigrams_list, foreign_nouns, results_file, i=1):
    for line in bigrams_list:
        line = line.rstrip()
        line = line.lower()
        adj, noun = line.split(' ')
        words = []
        if noun not in results_file:
            results_file[noun] = words
            results_file[noun].append(adj)

        if len(results_file[noun]) != i:
            if noun not in dictionary:
                results_file[noun].append(0)

            else:
                translation = dictionary[noun]
                for n in translation:
                    if n in foreign_nouns:
                        results_file[noun].append(foreign_word)
                        break
                if len(results_file[noun]) == i - 1:
                    results_file[noun].append('')
    return results_file


def main_file_same_language(foreign_word, bigrams_list, foreign_nouns, results_file, i=1):
    for line in bigrams_list:
        line = line.rstrip()
        line = line.lower()
        adj, noun = line.split(' ')
        words = []
        if noun not in results_file:
            results_file[noun] = words
            results_file[noun].append(adj)

        if len(results_file[noun]) != i:
            for n in foreign_nouns:
                if n == noun:
                    results_file[noun].append(foreign_word)
                    break
            if len(results_file[noun]) == i - 1:
                results_file[noun].append('')
    return results_file


# Функция делает масив, более удобный при записи в файл csv
def make_mas(lang, nouns_table, path=''):
    final_table = []
    not_translated_list = []
    i = 0
    for filename in os.listdir(path + 'result\\3_ready\\'):
        if filename[0:3] == lang:
            i += 1
    for element in nouns_table:
        a = ''
        j = 0
        for adjective in nouns_table[element]:
            if adjective == 0:
                j += 1
                a += ';'
            else:
                a += adjective + ';'
        if j == len(nouns_table[element]) - i:
            not_translated_list.append(element)
        else:
            final_table.append(element + ';' + a)
    return final_table, not_translated_list


if __name__ == '__main__':
    # Задайте язык, слово, его кириллический эквивалент(для русского)
    # и (опционально) путь, по которому расположены файлы биграмм
    language = sys.argv[1]
    word = sys.argv[2]
    if len(sys.argv) > 3:
        path_name = sys.argv[3] + '\\'
    else:
        path_name = ''

    result, nouns_no_translation = translate(language, word, path_name)
    write_file(language, word, nouns_no_translation, 'not_translated', path_name)
    write_file(language, word, result, '4_translated', path_name, 'csv')
