from copy import copy

from django.shortcuts import render, redirect
from django.conf import settings
from django import forms
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Post, Car
from .forms import PostModelForm
from .documents import UserDocument, CarDocument
from .serializers import CarSerializer

_BASE_DIR = settings.BASE_DIR

from middlevel.tasks import do_send_mail
def send_mail_to(request, subject, message, to):
    do_send_mail.delay(subject, message, to)
    return HttpResponse('Sent.')

##################################################################################

import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = CarSerializer
    document_class = CarDocument

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)



class SearchCars(PaginatedElasticSearchAPIView):
    def generate_q_expression(self, query):
        return Q('multi_match', query=query,
                fields=[
                    'id',
                    'name',
                    'color',
                    'description'
                ],
                minimum_should_match=1)




def add_car(request, name):
    Car.objects.create(name=name)
    return render(request, 'search.html')


from elasticsearch_dsl import Q
from .documents import Car
@csrf_exempt
def search(request):
    if request.method != 'POST':
        return render(request, 'search.html')
    Car.objects.create(name=request.POST['name'])
    #
    query = request.POST['search']
    q = Q(
        'multi_match',
        query=query,
        fields=[
        'name'
        ],
        fuzziness='auto'
    )
    search = CarDocument.search().query(q)
    response = search.execute()
    #
    for hit in search:
        print(hit)
    #
    response = CarSerializer(response, many=True)
    return HttpResponse(response.data)
##################################################################################


def login(request):
    print(request.GET)
    print(request.POST)
    print(request.FILES)
    return render(request, 'login.html')




def upload(request):
    # Post.objects.using('postgres').create(title='test-title')
    # open(settings.BASE_DIR / 'postgres.log', 'a').write(
    #     str(Post.objects.using('postgres').count())+'\n'+str(Post.objects.using('postgres').last())+'\n'
    # )
    
    # Post.objects.using('mysql').create(title='test-title')
    # open(settings.BASE_DIR / 'mysql.log', 'a').write(
    #     str(Post.objects.using('mysql').count())+'\n'+str(Post.objects.using('mysql').last())+'\n'
    # )
    
    """
    import pymongo
    client = pymongo.MongoClient('mongodb://mongodb:27017/default_mongo')
    #Define DB Name
    dbname = client['default_mongo']
    #Define Collection
    collection = dbname['default_mongo']
    mascot_1={
        "name": "Sammy",
        "type" : "Shark"
    }
    collection.insert_one(mascot_1)
    mascot_details = collection.find({})
    for r in mascot_details:
        print(r['name'])
    """
    
    form = PostModelForm()
    if request.method == 'GET':
        return render(request, 'app/upload.html', {'form': form})
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = PostModelForm()
            return render(request, 'app/upload.html', {'form': form})
        return render(request, 'app/upload.html', {'form': form})


class UploadForm(forms.Form):
    file = forms.FileField()


def upload_file(request):
    print('1.-')
    if request.method == "POST":
        print('2.-')
        handle_uploaded_file(request.FILES["file"])
        print('3.-')
        return redirect("/upload_file")
    print('4.-')
    return render(request, "app/upload.html", {'form': UploadForm(), 'path': 'upload_file'})


def handle_uploaded_file(f):
    print('5.-')
    with open(_BASE_DIR / "media/file_name", "wb+") as destination:
        for chunk in f.chunks():
            print('6.-')
            destination.write(chunk)