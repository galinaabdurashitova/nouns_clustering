import sys
import datetime
import os
from bigrams_preprocess import bigrams_preprocess
from morph_analyze import morph_analyze
from syntax_connection import syntax_check
from one_file import make_one_file
from grouping_nouns import classification_way_one_file as classification_way


def get_adjectives(path=''):
    adjectives = []
    with open(path + 'words.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip().split('\t')
            print(line)
            adjectives.append(line)
    return adjectives


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1] + '/'
    else:
        path = os.getcwd()
        path = path[0:path.rfind('\\')] + '\\'
        print(path)

    NAMES = get_adjectives(path)

    for wordline in NAMES:
        NAME = wordline[0]
        LANG = wordline[1]
        RUSSIAN = wordline[2]

        print(NAME)
        print(datetime.datetime.now())

        print('1. Обработка исходного файла биграмм, получение массива всех биграмм из файла')
        bigrams_preprocess(LANG, NAME, RUSSIAN, path)
        print(datetime.datetime.now())

        print('2. Обработка морфологическим анализатором')
        morph_analyze(LANG, NAME, path)
        print(datetime.datetime.now())

        print('3. Проверка биграмм на синтаксическую связь')
        syntax_check(LANG, NAME, RUSSIAN, path)
        print(datetime.datetime.now())

    print('4. Перевод')
    make_one_file(path)
    print(datetime.datetime.now())

    print('5. Алгоритмы классификации')
    classification_way(path)
    print(datetime.datetime.now())
