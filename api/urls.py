from django.urls import path
from . import views

urlpatterns = [
    path("obtain-token/", view=views.obtain_token, name="obtain_token"),
    path("joao/search/", view=views.joao_search, name="joao_search"),
    path('judite/<str:code>/passwd/', views.judite_passwd, name='judite_passwd'),
    path('token/remaining-time/', views.token_remaining_time, name='token_remaining_time'),
]
