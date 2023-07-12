from django.urls import path

from . import views
from .route import Route
from .controller import Controller, route, HttpResponse

# urlpatterns = []
# route = Route(urlpatterns)
# route.get('', Controller.index, 'index')

class PagesController(Controller):
    prefix_route = 'pages'
    
    @route('', 'GET', 'index-page', [9])
    def index(request):
        return HttpResponse('Index.')

urlpatterns = []
PagesController(urlpatterns)
# pages = PagesController(urlpatterns)
# urlpatterns.append(
#     path('', PagesController.index, name='index')
# )

# urlpatterns = [
#     path('', views.index),
# ]
