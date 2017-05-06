# 3. Проверка биграмм на соответствие прилагательное+существительное и на обладание синтаксической связью

import sys
import re
from functions import write_file


def syntax_check(lang, name, russian, path=''):
    if lang == 'rus':
        bigrams = rus_a_s(lang, name, russian, path)
    elif lang == 'eng':
        bigrams = eng_a_s(lang, name, path)
    elif lang == 'ger':
        bigrams = ger_a_s(lang, name, path)
    else:
        bigrams = []

    write_file(lang, name, bigrams, '3_ready', path)


# На выходе - массивы биграмм, соответствующих прилагательное+существительное
# и обладающих синтаксической связью

# RUS
# На входе - файл биграмм, преобработанный mystem
def rus_a_s(lang, name, russian, path=''):
    # while not os.path.exists('final/2_morph/' + LANG + '_' + NAME + '.txt'):
        # time.sleep(3)
    bigrams = []
    with open(path + 'result\\2_morph\\' + lang + '_' + name + '.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()

            if ' ' in line:
                line = line.split(' ')

                if '=A=' in line[0] and '=S,' in line[1]:
                    c = find_matches(line[0], line[1])

                    if c == 1:
                        line[0] = re.sub('^.*?{', '', line[0])
                        line[0] = re.sub('\??=.*$', '', line[0])
                        line[1] = re.sub('^.*?{', '', line[1])
                        line[1] = re.sub('\??=.*$', '', line[1])

                        if russian in line:
                            bigram = line[0] + ' ' + line[1]
                            if bigram not in bigrams:
                                bigrams.append(bigram)
    return bigrams


def find_matches(adj, noun):
    adjs = for_adjs(adj)
    nouns = for_nouns(noun)

    gender = ['муж', 'жен', 'сред']
    case = ['им', 'род', 'дат', 'вин', 'твор', 'пр']

    for variant_S in nouns:
        for variant_A in adjs:
            match_n = 0
            if 'ед' in variant_S and 'ед' in variant_A:
                match_n += 1
                for g in gender:
                    if g in variant_S and g in variant_A:
                        match_n += 1
            elif 'мн' in variant_S and 'мн' in variant_A:
                match_n += 2
            for c in case:
                if c in variant_S and c in variant_A:
                    match_n += 1
            if match_n == 3:
                return 1
    return 0


def for_adjs(adj):
    adj = re.sub('.*?{', '', adj)
    adj = adj.replace('}', '')
    adj = adj.split(u'|')
    adjs = []
    for element in adj:
        if 'A' in element:
            element = re.sub('^.*?A=', 'A=', element)
            adjs.append(element)
    return adjs


def for_nouns(noun):
    noun = re.sub('.*?{', '', noun)
    noun = noun.replace('}', '')
    noun = noun.split(u'|')
    nouns = []
    for element in noun:
        if 'S' in element:
            element = re.sub('^.*?S,', 'S,', element)
            nouns.append(element)
    return nouns


# ENG
# На входе - файл биграмм, преобработанный treetagger
def eng_a_s(lang, name, path=''):
    bigrams = []
    with open(path + 'result\\2_morph\\' + lang + '_' + name + '.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            line = re.sub('^;', '', line)
            adj, noun = line.split(';')
            adj = adj.split('\t')
            noun = noun.split('\t')

            if 'JJ' in adj[1] and noun[1] == 'NN':
                if adj[0] == name or adj[0] == name + 'er' or adj[0] == name + 'est':
                    bigram = adj[2] + ' '
                    if noun[2] != '<unknown>':
                        bigram += noun[2].lower()
                    else:
                        bigram += noun[0]
                    bigrams.append(bigram)
    return bigrams


# GER
# На входе - файл биграмм, преобработанный treetagger
def ger_a_s(lang, name, path=''):
    bigrams = []
    with open(path + 'result\\2_morph\\' + lang + '_' + name + '.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            line = re.sub('^;', '', line)
            adj, noun = line.split(';')
            adj = adj.split('\t')
            noun = noun.split('\t')

            if 'ADJ' in adj[1] and noun[1] == 'NN':
                if re.match(name + '(est|er)?e[rnms]?$', adj[0]):
                    bigram = adj[2] + ' '
                    if noun[2] != '<unknown>':
                        bigram += noun[2].lower()
                    else:
                        bigram += noun[0]
                    bigrams.append(bigram)
    return bigrams


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

    if language == 'rus':
        bigrams_checked = rus_a_s(language, word, russian_version, path_name)
    elif language == 'eng':
        bigrams_checked = eng_a_s(language, word, path_name)
    elif language == 'ger':
        bigrams_checked = ger_a_s(language, word, path_name)
    else:
        bigrams_checked = []
    write_file(language, word, bigrams_checked, '3_ready', path_name)
