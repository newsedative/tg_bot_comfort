# дополнения: отправка стикеров и музыки
import random
import os


def add_sticker():
    sticker_id = ['CAACAgIAAxkBAAEEm9tib5b2PBR8XrCgGzefs3hvhDbXjgACPRwAAlt3uEpBE2TisTtDdiQE',
                  'CAACAgIAAxkBAAEEm-Fib6CQ8a_iigbcs3RNAfqH6yZmlwACGxMAAifBcUnRvYBFTxWL5SQE',
                  'CAACAgIAAxkBAAEEm-dib6Gjjx07RZoEjZMXdZduZzrCewACAQEAAladvQoivp8OuMLmNCQE',
                  'CAACAgIAAxkBAAEEnkhicXdJvHnXYDqWv1ATMFI6692uSQACbgADwDZPE22H7UqzeJmXJAQ',
                  'CAACAgIAAxkBAAEEnlRicXfJgJp1RNNWl3VbHl5mrM0vwAACfk8CAAFji0YMX7n3Hno1B08kBA']
    return random.choice(sticker_id)


def add_music():
    DIR = 'music_of_nature'
    return os.path.join(random.choice(os.listdir(DIR)))

print(add_music())
