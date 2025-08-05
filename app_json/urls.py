from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_json, name='upload_json'),
    path('get_data/', views.show_data_from_db, name='show_data'),
]
