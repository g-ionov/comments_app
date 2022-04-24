from rest_framework import serializers
from .models import Article, Comment

class RecursiveCommentSerializer(serializers.Serializer):
    """Сериализация для дочерних комментариев внутри статьи
    (ограничивает вывод вложенных комментариев до 3 уровня)"""

    def to_representation(self, value):
        if value.level < 4:
            serializer = self.parent.parent.__class__(value, context=self.context)
            return serializer.data

class RecursiveCommentDetailSerializer(serializers.Serializer):
    """Сериализация для дочерних комментариев любой вложенности
    (используется для вывода всех вложенных комментариев для комментария 3 уровня)"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class FilterCommentSerializer(serializers.ListSerializer):
    """Фильтр комментариев, который ввыводит первыми только родительские комментарии
    (решает проблему с дублированием комментариев)"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    updated_at = serializers.DateTimeField(read_only=True, format="%d-%m-%Y %H:%M")
    user = serializers.SlugRelatedField('username', read_only=True,)
    child_comment = RecursiveCommentSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterCommentSerializer
        model = Comment
        fields = ('user', 'text', 'updated_at', 'child_comment')

class CommentDetailSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев неограниченной вложенности"""
    updated_at = serializers.DateTimeField(read_only=True, format="%d-%m-%Y %H:%M")
    user = serializers.SlugRelatedField('username', read_only=True,)
    child_comment = RecursiveCommentDetailSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterCommentSerializer
        model = Comment
        fields = ('user', 'text', 'updated_at', 'child_comment')

class CommentCreateSerializer(serializers.ModelSerializer):
    """Создание комментария к статье
    (также создание комментария в ответ на другой комментарий)"""

    """
    Кастомный валидатор, предназначенный для ограничения вложенности 
    при создании комментария по средствам POST запроса
    """
    # def validate_parent(self, data):
    #     if data.level:
    #         level = data.level
    #         if level > 2:
    #             raise serializers.ValidationError("Максимальная вложенность 3!!!")
    #     return data

    class Meta:
        model = Comment
        fields = ('article', 'parent', 'user', 'text')

class ArticleSerializer(serializers.ModelSerializer):
    """Сериализатор для статей
    (вывод списка и создание)"""
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    comment_count = serializers.IntegerField(source='get_count_comments', read_only=True)

    class Meta:
        model = Article
        fields = ('title', 'content', 'created_at', 'updated_at', 'comment_count')

class ArticleDetailSerializer(ArticleSerializer):
    """Сериализатор детальной информации о статье
    (с выводом комментариев)"""
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('title', 'content', 'created_at', 'updated_at', 'comment_count', 'comment')


