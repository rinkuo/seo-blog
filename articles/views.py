from django.shortcuts import render, redirect, get_object_or_404
from .models import *


def home(request):
    articles = Article.objects.all()
    ctx = {'articles': articles}
    return render(request, 'index.html', ctx)

def author_list(request):
    authors = Author.objects.all()
    ctx = {'authors': authors}
    return render(request, 'articles/author_list.html', ctx)

def author_create(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        description = request.POST.get('description')
        email = request.POST.get('email')
        if first_name and last_name and description and email:
            Author.objects.create(
                first_name=first_name,
                last_name=last_name,
                description=description,
                email=email,
            )
            return redirect('articles:home')
    return render(request, 'articles/create-author.html')

from django.utils.text import slugify

def blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_id = request.POST.get('author')
        image = request.FILES.get('image')

        if title and content and author_id and image:
            author = Author.objects.get(id=author_id)
            slug = slugify(title)

            # Ensure the slug is unique
            if Article.objects.filter(slug=slug).exists():
                slug = f"{slug}-{Article.objects.count() + 1}"

            Article.objects.create(
                title=title,
                content=content,
                author=author,
                image=image,
                slug=slug,
            )
            return redirect('articles:home')

    authors = Author.objects.all()
    ctx = {'authors': authors}
    return render(request, 'articles/create-article.html', ctx)


def blog_detail(request, year, month, day, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day
    )
    comments = Comment.objects.filter(article=article)

    related_articles = Article.objects.filter(author=article.author).exclude(pk=article.pk)

    ctx = {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
    }
    return render(request, 'articles/blog-detail.html', ctx)


def comment_create(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        if name and email and comment:
            Comment.objects.create(
                article=article,
                name=name,
                email=email,
                comment=comment,
            )
            return redirect('articles:success_commented', pk=article.pk)
    comments = Comment.objects.filter(article=article)
    ctx = {
        'article': article,
        'comments': comments,
    }
    return render(request, 'articles/blog-detail.html', ctx)

def success_commented(request, pk):
    article = get_object_or_404(Article, pk=pk)

    return render(request, 'articles/success-commented.html', {'article': article})


def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect('articles:home')