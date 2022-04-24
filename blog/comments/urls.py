from django.urls import path
from .views import ArticleListCreateView, CommentCreateView, CommentDetailView, ArticleDetailView

app_name = 'comments'
urlpatterns = [
    path('article/', ArticleListCreateView.as_view()),
    path('article/detail/<int:pk>', ArticleDetailView.as_view()),
    path('comment/create', CommentCreateView.as_view()),
    path('comment/detail/<int:pk>', CommentDetailView.as_view()),
]
