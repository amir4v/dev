import random

q_type = int(input('InterviewQ/1 or QinT/2 SoftSkills/3:'))
if q_type == 1:
    filename = './InterviewQ.txt'
elif q_type == 2:
    filename = './QinT.txt'
elif q_type == 3:
    filename = './SoftSkills.txt'

while 1:
    lines = open(filename, 'rt', encoding='utf-8').read().split('\n')
    print(lines[random.randint(0, len(lines))])
    input('>>>')
