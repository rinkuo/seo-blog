from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.home, name='home'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.author_create, name='author_create'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('article/delete/<int:pk>/', views.article_delete, name='article_delete'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/success/<int:pk>/', views.success_commented, name='success_commented'),
]
