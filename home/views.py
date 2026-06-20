from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def article_detail(request):
    return render(request, 'home/article_detail.html')

def category_detail(request):
    return render(request, 'home/related.html')
