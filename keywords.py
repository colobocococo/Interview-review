filename = "..//types//internal.txt"
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
internal_verbs = set(content.split())

filename = "..//types//external.txt"
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
external_verbs = set(content.split())

filename = "..//types//internal_phrases.txt"
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\n', ' ')
internal_phrases = list(content.split('. '))

filename = "..//types//external_words.txt"
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
external_words = set(content.split())
