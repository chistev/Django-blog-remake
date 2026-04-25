from django.shortcuts import render

def index(request):
    return render(request, 'home/article_detail1.html')