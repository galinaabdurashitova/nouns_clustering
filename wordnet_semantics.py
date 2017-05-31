# 6. Семантическая обработка с помощью WordNet

import os
import sys
from functions import write_file, check_arrays_for_commons
from nltk.corpus import wordnet as wn


def cluster_naming(path=''):
    wordlines = opening(path)
    clusters_with_names = clusters_search(wordlines)
    clusters_with_names = make_arr_for_write(clusters_with_names)
    write_file('all', 'languages', clusters_with_names, '6_classified', path_name, 'csv')


def opening(path=''):
    noun_lines = []
    with open(path + 'result\\5_classified\\all_bigrams.csv', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            words = line.split(';')
            noun = words[0]
            adjectives = words[1:]
            noun_lines.append([noun, adjectives])
    return noun_lines


def clusters_search(lines):
    noun_lines = []
    cluster = [lines[0][0]]
    last_adj_line = '1' * (len(lines[0][1]) - 1)
    i = 0
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
                cluster_name = another_try_three(cluster)
                if cluster_name == 'None':
                    i += 1
                noun_lines.append([cluster_name, last_adj_array, cluster])
                cluster = [line[0]]
        else:
            cluster.append(line[0])
        last_adj_array = line[1]
        last_adj_line = adj_line
    print(i)
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


def find_common_hypernym(nouns):
    hypernym = nouns[0]
    for i in range(1, len(nouns)):
        hypernyms1 = []
        hypernyms2 = []
        h1 = hypernym
        h2 = nouns[i]
        hypernyms1.append(h1)
        hypernyms2.append(h2)
        hypernym = check_arrays_for_commons(hypernyms1, hypernyms2)
        while not hypernym:
            if h1 is None:
                hypernym = h2[0]
                break
            elif h2 is None:
                hypernym = h1[0]
                break
            else:
                new_h1 = []
                for i in h1:
                    new_h1 = new_h1 + find_hypernym(i)
                h1 = new_h1
                new_h2 = []
                for i in h2:
                    new_h2 = new_h2 + find_hypernym(i)
                h2 = new_h2
                hypernyms1 = hypernyms1 + h1
                hypernyms2 = hypernyms2 + h2
            hypernym = check_arrays_for_commons(hypernyms1, hypernyms2)
    return hypernym


def another_try_one(nouns_cluster):
    all_hypernyms = {}
    for noun in nouns_cluster:
        hypernyms_array = []
        hypernyms = find_hypernym(noun)
        for i in range(0, 5):
            if hypernyms:
                hypernyms_array = hypernyms_array + hypernyms
                new_hypernyms = []
                for hypernym in hypernyms:
                    a = find_hypernym(hypernym)
                    if a:
                        new_hypernyms = new_hypernyms + a
                hypernyms = new_hypernyms
        for hyp in hypernyms_array:
            if hyp in all_hypernyms:
                all_hypernyms[hyp] += 1
            else:
                all_hypernyms[hyp] = 1

    i = 1
    best_match = 'None'
    # bad_names = ['abstraction', 'concept', 'idea', 'object']
    for hyp in all_hypernyms:
        # if hyp not in bad_names:
        if all_hypernyms[hyp] > i:
            best_match = hyp
            i = all_hypernyms[hyp]
    print(i, best_match)
    return best_match


def another_try_two(nouns_cluster):
    all_hypernyms = {}
    for noun in nouns_cluster:
        hypernyms_array = []
        hypernyms = find_hypernym(noun)
        for i in range(0, 5):
            if hypernyms:
                hypernyms_array = hypernyms_array + hypernyms
                new_hypernyms = []
                for hypernym in hypernyms:
                    a = find_hypernym(hypernym)
                    if a:
                        new_hypernyms = new_hypernyms + a
                hypernyms = new_hypernyms
        for hyp in hypernyms_array:
            if hyp in all_hypernyms:
                if noun not in all_hypernyms[hyp]:
                    all_hypernyms[hyp].append(noun)
            else:
                all_hypernyms[hyp] = [noun]

    best_match = 'None'
    # bad_names = ['abstraction', 'concept', 'idea', 'object']
    for hyp in all_hypernyms:
        # if hyp not in bad_names:
        if len(all_hypernyms[hyp]) == len(nouns_cluster):
            best_match = hyp
    print(best_match)
    return best_match


def another_try_three(nouns_cluster):
    all_hypernyms_count = {}
    all_hypernyms_nouns = {}
    for noun in nouns_cluster:
        hypernyms_array = []
        hypernyms = find_hypernym(noun)
        for i in range(0, 5):
            if hypernyms:
                hypernyms_array = hypernyms_array + hypernyms
                new_hypernyms = []
                for hypernym in hypernyms:
                    a = find_hypernym(hypernym)
                    if a:
                        new_hypernyms = new_hypernyms + a
                hypernyms = new_hypernyms

        for hyp in hypernyms_array:
            if hyp in all_hypernyms_count:
                all_hypernyms_count[hyp] += 1
            else:
                all_hypernyms_count[hyp] = 1
            if hyp in all_hypernyms_nouns:
                if noun not in all_hypernyms_nouns[hyp]:
                    all_hypernyms_nouns[hyp].append(noun)
            else:
                all_hypernyms_nouns[hyp] = [noun]

    best_match = 'None'
    # bad_names = ['abstraction', 'concept', 'idea', 'object']
    for hyp in all_hypernyms_nouns:
        # if hyp not in bad_names:
        if len(all_hypernyms_nouns[hyp]) == len(nouns_cluster):
            best_match = hyp
    if best_match == 'None':
        i = 1
        bad_names = ['act', 'abstraction', 'concept', 'group', 'idea', 'object', 'part']
        for hyp in all_hypernyms_count:
            if hyp not in bad_names:
                if all_hypernyms_count[hyp] > i:
                    best_match = hyp
                    i = all_hypernyms_count[hyp]
    print(best_match)
    return best_match


def make_arr_for_write(lines):
    result_file = []
    i = 0
    for line in lines:
        adjectives = line[1]
        nouns = line[2]
        for noun in nouns:
            line_noun_adjectives = str(i) + ';' + line[0] + ';' + noun
            for adj in adjectives:
                line_noun_adjectives += ';'
                line_noun_adjectives += adj
            result_file.append(line_noun_adjectives)
        i += 1
    return result_file


if __name__ == '__main__':
    # Задайте язык, слово, его кириллический эквивалент(для русского)
    # и (опционально) путь, по которому расположены файлы биграмм
    if len(sys.argv) > 1:
        path_name = sys.argv[1] + '\\'
    else:
        path_name = os.getcwd()
        path_name = path_name[0:path_name.rfind('\\')] + '\\'

    word_lines = opening(path_name)
    clusters_result = clusters_search(word_lines)
    clusters_result = make_arr_for_write(clusters_result)
    write_file('all', 'languages', clusters_result, '6_classified', path_name, 'csv')
