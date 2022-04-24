from rest_framework import generics
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentDetailSerializer, CommentCreateSerializer

class ArticleListCreateView(generics.ListCreateAPIView):
    """Просмотр списка статей с указанием колличества комментариев
    А также создание новой статьи"""
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class ArticleDetailView(generics.RetrieveAPIView):
    """Просмотр статьи (вывод комментариев ограничен 3 уровнем вложенности)"""
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer

class CommentCreateView(generics.CreateAPIView):
    """Создание комментария"""
    serializer_class = CommentCreateSerializer

class CommentDetailView(generics.RetrieveAPIView):
    """Предназначен для получения всех вложенных комментариев для комментария 3 уровня.
    (так как для вывода комментариев к статье по ТЗ установлено ограничение на вывод до 3 уровня)"""
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.filter(level=3)




