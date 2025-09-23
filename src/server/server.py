from razdel import tokenize, sentenize
from src.server.keywords import *
from src.server.utils import *
import matplotlib.pyplot as plt
import csv

check_true = ['Респондент', 'Interviewee', 'Interviewee:', 'Респондент:', 'SPEAKER_01', 'Спикер1']
check_false = ['Me', 'Интервьюер', 'Me:', 'Интервьюер:', 'SPEAKER_00', 'Спикер0']

verbs_i = dict()
verbs_not_i = dict()
verbs_e = dict()

words_i = dict()
words_e = dict()

count_i = dict()
count_we = dict()

verbs_self = dict()
verbs_other = dict()

def analyze(number):
    if (number in count_i):
        print("text number:", number, "was already analyzed!")
        return
    print("analyzing text number:", number)
    print("please wait...")
    filename = "..//files//txt//" + str(number) + ".txt"
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    flag = False
    new_content = ""
    for word in content.split():
        if word in check_true:
            flag = True
        if word in check_false:
            flag = False
        if flag:
            new_content += word + " "

    content = new_content
    file = content
    #print(content)

    sents = list(sentenize(content))

    text = []
    for sent in sents:
        new_sent = process(list(sent)[2])
        text.append(new_sent)

    cnt_i_phrases = 0
    for phrase in internal_phrases:
        cnt_i_phrases += file.count(phrase)


    cnt_internal, cnt_external = 0, 0
    words_in_text = 0
    cnt = 0
    cnt_reverse = 0
    cnt_other = 0
    cnt_i = 0
    cnt_we = 0
    cnt_verb_self = 0
    cnt_verb_other = 0
    for sent in text:
        for word in sent:
            words_in_text += 1
            if normal_form(word) in external_words:
                cnt += 1
            if normal_form(word) in internal_verbs:
                if 'я' in sent or 'Я' in sent or word[-1] in ['у', 'ю']:
                    cnt_internal += 1
                else:
                    cnt_other += 1

            if normal_form(word) in external_verbs:
                cnt_external += 1
            if word[-2:] == 'ся':
                #print(word)
                cnt_reverse += 1

            if word == 'я' or word == 'Я':
                cnt_i += 1
            if word == 'мы' or word == 'Мы':
                cnt_we += 1

            if part_of_speech(word) == 'VERB':
                if 'я' in sent or 'Я' in sent or word[-1] in ['у', 'ю']:
                    cnt_verb_self += 1
                else:
                    cnt_verb_other += 1



    #1
    #print("internal verbs frequency - ", (cnt_internal/words_in_text) * 100, "%")
    #print("not-self words frequency - ", (cnt_other / words_in_text) * 100, "%")

    verbs_i[number] = cnt_internal/words_in_text * 100
    verbs_not_i[number] = cnt_other/words_in_text * 100

    #2
    #print("internal phrases frequency - ", (cnt_i_phrases/words_in_text) * 100, "%")
    #print("external words frequency - ", (cnt/words_in_text) * 100, "%")

    words_i[number] = cnt_i_phrases/words_in_text * 100
    words_e[number] = cnt/words_in_text * 100

    #4
    #print("external verbs frequency - ", (cnt_external / words_in_text) * 100, "%")
    verbs_e[number] = cnt_external/words_in_text * 100

    #3
    #print("i frequency - ", (cnt_i / words_in_text) * 100, "%")
    #print("we frequency - ", (cnt_we / words_in_text) * 100, "%")

    count_i[number] = cnt_i/words_in_text * 100
    count_we[number] = cnt_we/words_in_text * 100

    #5
    #print("self verb frequency - ", (cnt_verb_self / words_in_text) * 100, "%")
    #print("other verb frequency - ", (cnt_verb_other / words_in_text) * 100, "%")

    verbs_self[number] = cnt_verb_self/words_in_text * 100
    verbs_other[number] = cnt_other/words_in_text * 100

    print("text number:", number, "was analyzed!")

mean_verbs_i = dict()
mean_verbs_not_i = dict()
mean_verbs_e = dict()

mean_words_i = dict()
mean_words_e = dict()

mean_count_i = dict()
mean_count_we = dict()

mean_verbs_self = dict()
mean_verbs_other = dict()

def change(array):
    n = len(array)
    mean = 0
    for i in range(1, 12):
        if i in array:
            mean += array[i]

    mean /= n

    mean_array = dict()
    for i in range(1, 12):
        if i in array:
            mean_array[i] = array[i]/mean

    return mean_array

def mean_all():
    global mean_verbs_i
    mean_verbs_i = change(verbs_i)
    global mean_verbs_not_i
    mean_verbs_not_i = change(verbs_not_i)
    global mean_verbs_e
    mean_verbs_e = change(verbs_e)

    global mean_words_i
    mean_words_i = change(words_i)
    global mean_words_e
    mean_words_e = change(words_e)

    global mean_count_i
    mean_count_i = change(count_i)
    global mean_count_we
    mean_count_we = change(count_we)

    global mean_verbs_self
    mean_verbs_self = change(verbs_self)
    global mean_verbs_other
    mean_verbs_other = change(verbs_other)

def inner_indicator(number):
    k1 = 3
    k2 = 4
    k3 = 1
    k4 = 2
    return (k1 * mean_verbs_i[number] +
            k2 * mean_words_i[number] +
            k3 * mean_count_i[number] +
            k4 * mean_verbs_self[number]) / (k1 + k2 + k3 + k4)

def outer_indicator(number):
    k1 = 4
    k2 = 4
    k3 = 4
    k4 = 1
    k5 = 2
    return (k1 * mean_verbs_not_i[number] +
            k2 * mean_verbs_e[number] +
            k3 * mean_words_e[number] +
            k4 * mean_count_we[number] +
            k5 * mean_verbs_other[number]) / (k1 + k2 + k3 + k4 + k5)

def average_indicator(number):
    mean_all()
    if number not in mean_verbs_i:
        print("text number:", number, "doesn't exist!")
        return
    print("net reference =", inner_indicator(number) - outer_indicator(number))

def internal_data():
    mean_all()
    X = []
    Y = [[] for i in range(4)]
    for number in mean_verbs_self:
        #print(number, mean_verbs_self[number])
        X.append(number)
        Y[0].append(mean_verbs_i[number])
        Y[1].append(mean_words_i[number])
        Y[2].append(mean_count_i[number])
        Y[3].append(mean_verbs_self[number])

    #return
    for i in range(4):
        plt.plot(X, Y[i])
    plt.title('Internal reference parameters')
    plt.xlabel('Person number')
    plt.ylabel('Coefficient')

    plt.grid()
    plt.legend(['управляющие глаголы', 'ключевые слова', 'местоимения', 'субъект действий'])
    plt.show()

def external_data():
    mean_all()
    X = []
    Y = [[] for i in range(5)]
    for number in mean_verbs_other:
        X.append(number)
        Y[0].append(mean_verbs_not_i[number])
        Y[1].append(mean_words_e[number])
        Y[2].append(mean_verbs_e[number])
        Y[3].append(mean_count_we[number])
        Y[4].append(mean_verbs_other[number])

    for i in range(5):
        plt.plot(X, Y[i])
    plt.title('External reference parameters')
    plt.xlabel('Person number')
    plt.ylabel('Coefficient')

    plt.grid()
    plt.legend(['управляющие глаголы', 'ключевые слова', 'глаголы-признаки командной работы',
                'местоимения', 'субъект действий'])
    plt.show()

