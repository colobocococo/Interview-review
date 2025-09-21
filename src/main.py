from server import *


while True:
    print('ask a question: A for analyze text, S for show analysis, Q for quit')
    q = input()
    if q == 'A':
        print('give number of text to analyze')
        number = int(input())
        analyze(number)
    elif q == 'S':
        print('give number of text to show analysis')
        number = int(input())
        average_indicator(number)
    elif q == 'Q':
        print('quit')
        break
    else:
        print('error')
        exit()

for i in range(1, 12):
    analyze(i)

internal_data()
external_data()
