from django.urls import path
from . import views

urlpatterns = [
    path("joao/search/", view=views.joao_search, name="joao_search"),
    path('judite/<str:code>/passwd/', views.judite_passwd, name='judite_passwd'),
]
