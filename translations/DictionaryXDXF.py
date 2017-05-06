
class DictionaryXDXF:
    def __init__(self, lang1, lang2, ready=False, path=''):
        dicti = {}
        with open(path + 'dictionaries\\XDXF_preprocessed\\d_' + lang1 + '_' + lang2 + '.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if not ready:
                    self.preprocess(line)
                line = line.rstrip()
                word, definition = line.split(';')
                definition.split(',')
                dicti[word] = definition
        self.dictionary = dicti

    def preprocess(self, line):
        return line + 'Я не написала функцию'

    def find_translation(self, word):
        if word in self.dictionary:
            if len(self.dictionary[word]) > 0:
                return self.dictionary[word]
        else:
            return False
