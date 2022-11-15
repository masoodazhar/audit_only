from django.shortcuts import render

def index(request):
    return render(request, 'dashboard.html')


def soon(request):
    return render(request, 'soon.html')