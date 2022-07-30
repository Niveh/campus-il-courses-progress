
def translate(sentence):
    translation = ""
    words = {'esta': 'is', 'la': 'the', 'en': 'in',
             'gato': 'cat', 'casa': 'house', 'el': 'the'}

    words_gen = (word for word in sentence.split(" "))
    try:
        while True:
            translation += words[next(words_gen)] + " "

    except:
        return translation


print(translate("el gato esta en la casa"))
