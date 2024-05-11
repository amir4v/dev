import random

q_type = int(input('InterviewQ/1 or QinT/2'))
if q_type == 1:
    filename = './InterviewQ.txt'
else:
    filename = './QinT.txt'

while 1:
    lines = open(filename, 'rt', encoding='utf-8').read().split('\n')
    print(lines[random.randint(0, len(lines))])
    input('>>>')
