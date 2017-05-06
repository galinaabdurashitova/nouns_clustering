# Получить ключ по адресу https://developers.lingvolive.com/
# Ключ действует 1 сутки
# Нужно подключение к интернету
import requests


class AbbyyLingvoApi:
    def __init__(self, lang1, lang2, key):
        self.bearer_token = requests.post('https://developers.lingvolive.com/api/v1.1/authenticate',
                                          headers={'Authorization': 'Basic ' + key}).text
        self.lang1 = self.get_language_number(lang1)
        self.lang2 = self.get_language_number(lang2)

    def find_translation(self, word):
        translation = requests.get('https://developers.lingvolive.com/api/v1/Minicard?text=' + word +
                                   '&srcLang=' + self.lang1 + '&dstLang=' + self.lang2,
                                   headers={'Authorization': 'Bearer ' + self.bearer_token}).json()
        if type(translation) != dict:
            return False
        translation = translation['Translation']['Translation']
        translation = translation.replace(',', ';').split('; ')
        return translation

    def get_language_number(self, lang):
        if lang == 'rus':
            return '1049'
        elif lang == 'eng':
            return '1033'
        elif lang == 'ger':
            return '1031'


if __name__ == '__main__':
    key_now = 'Nzc5NzFiOTItNzdlNi00NmU1LTljNzMtYTU2OWE3ZDE1NzhmOmU1MDAzNWQxOGZlYTQ5OTI4YjFhZWU5NWVkNjE4ZDRm'
    a = AbbyyLingvoApi('rus', 'eng', key_now)
    print(a.find_translation('аааааутро'))
