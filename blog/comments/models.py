from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class Article(models.Model):
    """Статья"""
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    """Подсчет количества комментариев к статье"""
    def get_count_comments(self):
        return self.comment.all().count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['title']

class AbstractComment(models.Model):
    """Абстрактная модель комментария"""

    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        abstract = True

class Comment(AbstractComment, MPTTModel):
    """Комментарий"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', on_delete=models.CASCADE, null=True, blank=True, related_name='child_comment')

    """
    Альтернативный вариант ограничения уровня вложенности комментариев 
    (вместо валидации поля paren внути CommentCreateSerializer)
    Отличается тем, что при наличии этого метода будет отсутсвовать возможность добавления 
    комментария любой вложенности через админку
    """

    # def save(self, *args, **kwargs):
    #     if self.parent.level > 2:
    #         raise ValueError("Максимальная вложенность 3!")
    #     else:
    #         super().save(*args, **kwargs)

    def __str__(self):
        return '%s - %s: %s' % (self.article, self.user, self.updated_at)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['updated_at']

