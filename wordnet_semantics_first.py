# 6. Семантическая обработка с помощью WordNet

import os
import sys
from functions import write_file, check_arrays_for_commons
from grouping_nouns import make_categories
from nltk.corpus import wordnet as wn


def cluster_naming(path=''):
    wordlines = opening(path)
    # clusters_with_names = clusters_search(wordlines)
    # clusters_with_names = make_arr_for_write(clusters_with_names)
    # write_file('all', 'languages', clusters_with_names, '6_classified', path_name, 'csv')


def opening(path=''):
    noun_lines = []
    with open(path + 'result\\4_translated\\all_languages.csv', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            words = line.split(';')
            noun = words[0]
            adjectives = words[1:]
            noun_lines.append([noun, adjectives])
    return noun_lines


def find_hypernym(noun):
    if len(wn.synsets(noun)) > 0:
        synset = wn.synsets(noun)[0]
        if len(synset.hypernyms()) > 0:
            hypernyms = synset.hypernyms()
            lemmas = []
            for hypernym in hypernyms:
                lemmas.append(hypernym.lemmas()[0].name())
            return lemmas
    else:
        return None


def find_definition(all_nouns):
    bad_names = ['act', 'abstraction', 'concept', 'group', 'idea', 'object', 'part', 'other']
    clusters = {}
    for noun in all_nouns:
        if noun[0] != '':
            hypernym = [noun[0]]
            hyper = check_arrays_for_commons(hypernym, bad_names)
            i = 0
            while not hyper:
                # print(hypernym)
                hypernym_new = []
                for hyp in hypernym:
                    h = find_hypernym(hyp)
                    if h:
                        hypernym_new = hypernym_new + h
                if not hypernym_new:
                    hypernym = ['other']
                else:
                    hypernym = hypernym_new
                i += 1
                if i >= 8:
                    hyper = 'other'
                else:
                    hyper = check_arrays_for_commons(hypernym, bad_names)
            if hyper not in clusters:
                clusters[hyper] = []
            clusters[hyper].append(noun)
    return clusters


def find_common(nouns_list):
    clusters = {}
    for line in nouns_list:
        hypernym = [line[0]]
        for i in range(0, 3):
            if hypernym:
                hypernym = find_hypernym(hypernym[0])
        if not hypernym:
            hypernym = ['other']
        if hypernym[0] not in clusters:
            clusters[hypernym[0]] = []
        clusters[hypernym[0]].append(line)
    return clusters


def clusters_search(lines):
    noun_lines = []
    cluster = [lines[0][0]]
    last_adj_line = '1' * (len(lines[0][1]) - 1)
    last_adj_array = []
    for line in lines:
        adj_line = ''
        for adj in line[1]:
            if adj != '':
                adj_line += '1'
            else:
                adj_line += '0'
        if adj_line != last_adj_line:
            if len(cluster) > 0:
                noun_lines.append([last_adj_array, cluster])
                cluster = [line[0]]
        else:
            cluster.append(line[0])
        last_adj_array = line[1]
        last_adj_line = adj_line
    return noun_lines


if __name__ == '__main__':
    # Задайте язык, слово, его кириллический эквивалент(для русского)
    # и (опционально) путь, по которому расположены файлы биграмм
    if len(sys.argv) > 1:
        path_name = sys.argv[1] + '\\'
    else:
        path_name = os.getcwd()
        path_name = path_name[0:path_name.rfind('\\')] + '\\'

    word_lines = opening(path_name)
    clusters_result = find_common(word_lines)
    clusters_lines = []
    i = 1
    for cluster in clusters_result:
        cl = []
        for noun in clusters_result[cluster]:
            adj = ''
            for a in noun[1]:
                adj = adj + ';' + a
            cl.append(noun[0] + adj)
        cl = make_categories(cl, os.listdir(path_name + 'result\\3_ready\\'), 0)
        for line in cl:
            clusters_lines.append(str(i) + ';' + cluster + ';' + line)
        i += 1
        # print(line, len(clusters_result[line]))
    print(len(clusters_result))
    write_file('all', 'languages', clusters_lines, '7_classified', path_name, 'csv')
