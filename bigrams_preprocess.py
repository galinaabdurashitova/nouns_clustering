# 1. Обработка биграмм

import sys
from functions import write_file


def bigrams_preprocess(lang, name, russian, path=''):
    bigrams = make_bigrams(lang, name, russian, path)
    write_file(lang, name, bigrams, '1_adj_noun', path)


# На выходе массив из биграмм, где первое слово - adj, а второе - noun
def make_bigrams(lang, name, russian, path=''):
    b = []
    with open(path + 'bigram_files\\googlebooks-' + lang + '-all-2gram-20120701-' + name[0:2],
              'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            line = line.replace('\t', ' ')
            line = line.lower()
            if lang == 'rus':
                if russian[0:-3] in line:
                    r = line.split(' ')
                    if '_' in r[0] and '_' in r[1]:
                        r1 = r[0].split(u'_')
                        r2 = r[1].split(u'_')
                        if r1[1] == 'adj' and r2[1] == 'noun' and r2[0] != '':
                            a = r1[0] + ' ' + r2[0]
                            if a not in b:
                                b.append(a)
            else:
                if name in line:
                    r = line.split(' ')
                    if '_' in r[0] and '_' in r[1]:
                        r1 = r[0].split(u'_')
                        r2 = r[1].split(u'_')
                        if r1[1] == 'adj' and r2[1] == 'noun' and r2[0] != '':
                            a = r1[0] + ' ' + r2[0]
                            if a not in b:
                                b.append(a)
    return b


if __name__ == '__main__':
    # Задайте язык, слово, его кириллический эквивалент(для русского)
    # и (опционально) путь, по которому расположены файлы биграмм
    language = sys.argv[1]
    word = sys.argv[2]
    russian_version = sys.argv[3]
    if len(sys.argv) > 4:
        path_name = sys.argv[4] + '\\'
    else:
        path_name = ''

    bigrams_processed = make_bigrams(language, word, russian_version, path_name)
    write_file(language, word, bigrams_processed, '1_adj_noun', path_name)
