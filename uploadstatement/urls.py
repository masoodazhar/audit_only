from django.urls import path
from .views import (
    uploadstatement,
    search,
    index,
    convert_bank_statement
)


urlpatterns = [
    path('', search, name='search'),
    path('t/', index, name='index'),
    path('upload/', uploadstatement, name='uploadstatement'),
    path('ConvertBank/', convert_bank_statement, name='convert_bank_statement')
    
]
