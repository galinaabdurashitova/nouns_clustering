# Получить ключ по адресу https://tech.yandex.ru/keys/?service=trnsl
# Нужно подключение к интернету
import requests


class YandexApi:
    def __init__(self, lang1, lang2, key):
        self.key = key
        self.langs = self.get_language_number(lang1) + '-' + self.get_language_number(lang2)

    def find_translation(self, word):
        translation = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?'
                                   'key=' + self.key +
                                   '&text=' + word +
                                   '&lang=' + self.langs).json()

        translation = translation['text'][0].lower()
        translation = translation.split(' ')
        # return translation
        if len(translation) == 1:
            return translation
        elif len(translation) == 2:
            translation = translation[1]
            return translation.split(' ')
        else:
            return translation[-1].split(' ')

    def get_language_number(self, lang):
        if lang == 'rus':
            return 'ru'
        elif lang == 'eng':
            return 'en'
        elif lang == 'ger':
            return 'de'


if __name__ == '__main__':
    key_now = 'trnsl.1.1.20170424T150123Z.ca89cfc1fa375d15.b3a867406943f8f73026d936eb06895f1e645495'
    a = YandexApi('rus', 'eng', key_now)
    print(a.find_translation('замок'))
