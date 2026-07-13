from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from home.models import Article, Category, Like
from django.http import JsonResponse
from django.db.models import Q

def index(request):
    articles_list = Article.objects.filter(is_published=True)
    # You create a paginator with all articles
    paginator = Paginator(articles_list, 6) # Splits into pages of 6
    
    page = request.GET.get('page')
    
    try:
        # Then you ask for a specific page
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
         # If page is out of range, deliver last page of results
        articles = paginator.page(paginator.num_pages)
        
    liked_articles = []
    if request.user.is_authenticated:
        liked_articles = Like.objects.filter(user=request.user).values_list('article_id', flat=True)
    
    return render(request, 'home/index.html', {'articles':articles, 'liked_articles': liked_articles})

def article_detail(request):
    return render(request, 'home/article_detail.html')

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    articles_list = Article.objects.filter(category=category, is_published=True)
    
    paginator = Paginator(articles_list, 6)
    page = request.GET.get('page')
    
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    liked_articles = []
    if request.user.is_authenticated:
        liked_articles = Like.objects.filter(user=request.user).values_list('article_id', flat=True)
    
    total_articles = articles_list.count()
    
    return render(request, 'home/related.html', {
        'category': category,
        'articles': articles,
        'liked_articles': liked_articles,
        'total_articles': total_articles,
    })

def search(request):
    query = request.GET.get('q', '') # query = '' when no parameter
    
    results = []
    results_count = 0
    
    if query:
        # This searches for articles where ANY condition is true
        # WITHOUT Q - AND condition (ALL must be true)
        results = Article.objects.filter(
            Q(title__icontains=query) | # OR
            Q(content__icontains=query) | # OR
            Q(category__name__icontains=query),
            is_published=True # ← AND condition
        ).distinct() # WITHOUT .distinct() An article that matches MULTIPLE conditions would appear as many times!
        
        results_count = results.count()
        
        paginator = Paginator(results, 6)
        page = request.GET.get('page')
        
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
    
    else:
        articles = []
        
    liked_articles = []
    if request.user.is_authenticated:
        liked_articles = Like.objects.filter(user=request.user).values_list('article_id', flat=True)
    
    
    return render(request, 'home/search.html', {
        'articles':articles,
        'query':query,
        'results_count':results_count,
        'liked_articles': liked_articles
    })
    
@login_required
@require_POST
def toggle_like(request):
    article_id = request.POST.get('article_id')
    
    if not article_id:
        return JsonResponse({'error': 'Article ID is required'}, status=400)
    
    article = get_object_or_404(Article, id=article_id)
    
    like, created = Like.objects.get_or_create(
        user=request.user,
        article=article
    )
    
    if not created:
        # User already liked it, so unlike it
        like.delete()
        liked = False
    else:
        
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': article.total_likes()
    })