# 2. Проверка биграмм морфологическим анализатором

import os
import sys
import time


def morph_analyze(lang, name, path=''):
    if not os.path.exists(path + 'result\\2_morph\\'):
        os.makedirs(path + 'result\\2_morph\\')
    if lang == 'rus':
        mystem(lang, name, path)
    elif lang == 'eng' or lang == 'ger':
        treetagger(lang, name, path)


# Для русского языка используется mystem
def mystem(lang, name, path=''):
    input_path = path + 'result\\1_adj_noun\\' + lang + '_' + name + '.txt'
    output_path = path + 'result\\2_morph\\' + lang + '_' + name + '.txt'
    os.system(path + 'mystem\\mystem.exe -ci -e utf-8 ' + input_path + ' ' + output_path)
    while not os.path.exists(output_path):
        time.sleep(3)
    time.sleep(3)


# Для английского и немецкого используется treetagger
def treetagger(lang, name, path=''):
    if not os.path.exists(path + 'result\\tmp\\preTT\\'):
        os.makedirs(path + 'result\\tmp\\preTT\\')
    if not os.path.exists(path + 'result\\tmp\\postTT\\'):
        os.makedirs(path + 'result\\tmp\\postTT\\')
    tr_begin(lang, name, path)
    input_path = path + 'result\\tmp\\preTT\\' + lang + '_' + name + '.txt'
    output_path = path + 'result\\tmp\\postTT\\' + lang + '_' + name + '.txt'
    if lang == 'eng':
        lang_param = path + 'TreeTagger\\lib\\english-utf8.par'
    elif lang == 'ger':
        lang_param = path + 'TreeTagger\\lib\\german-utf8.par'
    else:
        lang_param = path + 'TreeTagger\\lib\\english-utf8.par'
    os.system(path + 'TreeTagger\\bin\\tree-tagger.exe -token -lemma '
              + lang_param + ' ' + input_path + ' ' + output_path)
    while not os.path.exists(output_path):
        time.sleep(3)
    time.sleep(3)
    tr_end(lang, name, path)


def tr_begin(lang, name, path=''):
    lines_words_split = ''
    with open(path + 'result\\1_adj_noun\\' + lang + '_' + name + '.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if ' ' in line and name in line:
                line = line.split(' ')
                if line[1] != '':
                    lines_words_split = lines_words_split + line[0] + '\n' + line[1]
    with open(path + 'result\\tmp\\preTT\\' + lang + '_' + name + '.txt', 'w', encoding='utf-8') as d:
        d.write(lines_words_split)


def tr_end(lang, name, path=''):
    # while not os.path.exists(u'final/2_morph/' + LANG + '_' + NAME + u'.txt'):
        # t = ''
    # time.sleep(3)
    lines_words_connect = ''
    with open(path + 'result\\tmp\\postTT\\' + lang + '_' + name + '.txt', 'r', encoding='utf-8') as f:
        i = 1
        for line in f:
            if i % 2 != 0:
                line = line.rstrip()
                lines_words_connect = lines_words_connect + line + ';'
            else:
                lines_words_connect += line
            i += 1
    with open(path + 'result\\2_morph\\' + lang + '_' + name + '.txt', 'w', encoding='utf-8') as d:
        d.write(lines_words_connect)


if __name__ == '__main__':
    # Задайте язык, слово
    # и (опционально) путь, по которому расположены файлы биграмм
    language = sys.argv[1]
    word = sys.argv[2]
    if len(sys.argv) > 3:
        path_name = sys.argv[3] + '\\'
    else:
        path_name = ''
    if not os.path.exists(path_name + 'result\\2_morph'):
        os.makedirs(path_name + 'result\\2_morph\\')

    if language == 'rus':
        mystem(language, word, path_name)
    elif language == 'eng' or language == 'ger':
        treetagger(language, word, path_name)
