from django import template

register = template.Library()

BAD_WORDS = ['как', 'гаджет', 'редиска', 'fuck',
             'shit', 'мы считаем', 'логично', 'юните', 'очевидным']
SYMBOLS = ['!', '?', ':', '.', ',', ';', '«', '»']


@register.filter()
def censor(value, censored_words=BAD_WORDS, symbols=SYMBOLS):
    if isinstance(value, str):
        for i in value.split():
            count = 0
            if not i.isalnum():
                for j in symbols:
                    if j in i:
                        count += 1
            if i[:len(i) - count].lower() in censored_words:
                value = value.replace(i[:len(i) - count], i[0] + '*' * (len(i) - 1 - count))
    else:
        try:
            raise AttributeError
        except AttributeError:
            print("AttributeError")
    return value

