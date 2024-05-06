import random

filename = './InterviewQ.txt'
filename = './QinT.txt'

while 1:
    lines = open(filename, 'rt', encoding='utf-8').read().split('\n')
    print(lines[random.randint(0, len(lines))])
    input('>>>')
