from django.urls import path
from .views import (
    uploadstatement,
    search,
    index
)


urlpatterns = [
    path('', search, name='search'),
    path('t/', index, name='index'),
    path('upload', uploadstatement, name='uploadstatement'),
    
]
