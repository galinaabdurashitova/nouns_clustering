
class DictionaryTxt:
    def __init__(self, lang1, lang2, path=''):
        dicti = {}
        with open(path + 'dictionaries\\simple\\' + lang1 + '_' + lang2 + '.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip()
                word, pos, definition, dict_type = line.split('\t')
                definition.split(',')
                dicti[word] = definition
        self.dictionary = dicti

    def find_translation(self, word):
        if word in self.dictionary:
            if len(self.dictionary[word]) > 0:
                return self.dictionary[word]
        else:
            return False