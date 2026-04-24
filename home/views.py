from django.shortcuts import render

def index(request):
    return render(request, 'home/search1.html')