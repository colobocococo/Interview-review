import pymorphy2_dicts_ru
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


number = 5
name = str(number) + ".txt"
f = open(name, "r", encoding="utf-8")

inter = ['я']
exter = ['мне', 'мной', 'мною', 'меня']

flag_false = ['Интервьюер', 'Me']
flag_true = ['Респондент', 'Interviewee']

end_word = [',', ';', '.', '!', '?', ':']

def first_change(str):
    if str[-1] in end_word:
        return str[:-1]
    return str

def parser(str):
    return morph.parse(str)[0]

def part(str):
    return parser(str).tag.POS

def norm(str):
    return parser(str).normal_form

def need(str):
    if (part(str)) == 'VERB' or norm(str) == 'я':
        return 1
    return 0


txt = []
flag = 0
for string in f:
    for word in string.split():
        word = first_change(word)

        if word in flag_true:
            flag = 1
        if word in flag_false:
            flag = 0

        if need(word) and flag == 1:
            txt.append(word)

a = 0
b = 0
for i in range(len(txt) - 2):
    if (part(txt[i]) == 'VERB' or part(txt[i+2]) == 'VERB') and norm(txt[i+1]) == 'я':
        if txt[i+1] == 'я':
            a += 1
        else:
            b += 1

print('Внутренняя референция -', str(a) + ', внешняя референция -', str(b) + ';')
print('Соотношение:', round(a/b, 2))




