from django.db import connection
from django.shortcuts import render
from .models import Link


def search(request):
    name = request.GET.get('name')
    
    if not name:
        return render(request, 'app/search.html')
    
    name = name.strip()
    if ' ' in name:
        names = name.split(' ')
        name = '%'.join(names).lower()
    
    cursor = connection.cursor()
    sql = f"SELECT * FROM app_link WHERE lower(url) LIKE '%{name}%'"
    cursor.execute(sql)
    urls = cursor.fetchall()
    
    return render(request, 'app/result.html', {'urls': urls})


def watch(request):
    url = request.POST.get('url')
    return render(request, 'app/watch.html', {'url': url})