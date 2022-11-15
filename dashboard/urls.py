from django.urls import path, include
from django.shortcuts import render
from .views import index, soon

urlpatterns = [
    path('', index, name='dashboard'),
    path('work-in-progress-1/', soon, name='soon1'),
    path('work-in-progress-2/', soon, name='soon2'),
    path('work-in-progress-3/', soon, name='soon3'),
    path('work-in-progress-4/', soon, name='soon4'),
    path('work-in-progress-5/', soon, name='soon5'),
    path('work-in-progress-6/', soon, name='soon6'),
]
