from django.urls import path
from . import views

urlpatterns = [
    path("judite/<int:judite_id>/", view=views.judite, name="judite"),
    path("import_data_model/", view=views.import_data_model, name="imp_data"),
    path("export_data_model/", view=views.export_data_model, name="exp_data"),
    path("api/joao_search/", view=views.api_search_joao, name="api_joao_search"),
]
