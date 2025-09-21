import pymorphy2
morph = pymorphy2.MorphAnalyzer()

def parsed(word):
    return morph.parse(word)[0]

def part_of_speech(word):
    p = parsed(word)
    return p.tag.POS

def clean(word):
    if word[-1] in [',', '.', ':', ',', ';', ':', '!', '?']:
        word = word[:-1]
    return word

def normal_form(word):
    p = parsed(word)
    return p.normal_form

def process(sent):
    new_sent = []
    for word in sent.split():
        word = clean(word)
        new_sent.append(word)

    return new_sent