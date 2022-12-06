from random import sample, shuffle
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from .models import Word


# One Time Running
filename = 'ALL-(Ultimate)-(SpuerUseful) - (A1-C2) + (4000) + (10,000 Longman) + (10,000 Common etc) + (10,000 Common) - EN-FA.txt'
TEST = False # if True, app won't show translation
print(f'⬤ FILENAME: {filename}')
print(f'⬤ TEST = {TEST}')
re_new = 0
#


def get_file_words():
    lines = open(settings.WORDS_DIR / filename, 'r', encoding='utf-8').readlines()
    words = [
        (
            line.split('  ->  ')[0],
            line.strip('\n')
        ) for line in lines
    ]
    shuffle(words)
    return words


def home(request):
    global re_new
    
    count = request.POST.get('count', None)
    
    # least_seen = Word.objects.all().order_by('seen').first().seen
    # words = Word.objects.filter(seen=least_seen).order_by('?')[:10]
    words = Word.objects.all().order_by('?')[:10]
    
    # print(
        # least_seen,
        # '-',
        # Word.objects.filter(seen=least_seen).count()
    # )
    
    if count == 'YES':
        re_new += 1
        for word in words:
            word.seen += 1
        Word.objects.bulk_update(words, fields=['seen'])
    
    # TEST
    if TEST:
        for word in words:
            word.line = word.word
    
    context = {'words': sample(list(words), 10), 're_new': re_new}
    return render(request, 'app/home.html', context)


def refresh(request):
    Word.objects.all().delete()
    
    words = get_file_words()
    Word.objects.bulk_create([
        Word(word=word[0], line=word[1]) for word in words
    ])
    
    return HttpResponse("Refreshed.")
