# 5. Алгоритмы группировки

import os
import sys
from functions import write_file


def classification_way_one_file(path=''):
    noun_lines = opening('all', 'languages', path)
    noun_lines = make_categories(noun_lines, os.listdir(path + 'result\\3_ready\\'), 0)
    write_file('all', 'bigrams', noun_lines, '5_classified', path, 'csv')


def classification_way_separate_files(lang, name, path=''):
    noun_lines = opening(lang, name, path)
    noun_lines = make_categories(noun_lines, os.listdir(path + 'result\\4_translated\\'), 0)
    write_file(lang, name, noun_lines, '5_classified', path, 'csv')


def opening(lang, name, path=''):
    noun_lines = []
    with open(path + 'result\\4_translated\\' + lang + '_' + name + '.csv', 'r', encoding='utf-8') as f:
        for line in f:
            noun_lines.append(line.rstrip())
    return noun_lines


# Алгоритм, группирующий существительные по прилагательным, с которыми они сочетаются
def make_categories(noun_lines, filenames, i=0):
    if i >= len(filenames):
        return noun_lines
    mas1 = []
    mas2 = []
    n = filenames[i]
    for element in noun_lines:
        adjectives = element.split(';')
        if n[4:-4] in adjectives[1:]:
            mas1.append(element)
        else:
            mas2.append(element)
    mas1 = make_categories(mas1, filenames, i + 1)
    mas2 = make_categories(mas2, filenames, i + 1)
    mas = mas1 + mas2
    return mas


if __name__ == '__main__':
    # Задайте язык, слово, его кириллический эквивалент(для русского)
    # и (опционально) путь, по которому расположены файлы биграмм
    language = sys.argv[1]
    word = sys.argv[2]
    if len(sys.argv) > 3:
        path_name = sys.argv[3] + '\\'
    else:
        path_name = os.getcwd()
        path_name = path_name[0:path_name.rfind('\\')] + '\\'

    # classification_way_one_file(path_name)
    nouns = opening(language, word, path_name)
    nouns = make_categories(nouns, os.listdir(path_name + 'result\\4_translated\\'), 0)
    write_file(language, word, nouns, '5_classified', path_name, 'csv')
