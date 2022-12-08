from django.urls import path
from .views import (
    uploadstatement,
    search,
    dashboard_audit,
    convert_bank_statement
)


urlpatterns = [
    path('', search, name='search'),
    path('test/', dashboard_audit, name='indexView'),
    path('upload/', uploadstatement, name='uploadstatement'),
    path('ConvertBank/', convert_bank_statement, name='convert_bank_statement')
    
]
