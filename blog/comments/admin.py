from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Article, Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'updated_at')
    list_display_links = ('title', )
    search_fields = ('title', 'content', 'created_at', 'updated_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'parent', 'text', 'created_at', 'updated_at')
    search_fields = ('article', 'user', 'parent', 'text', 'created_at', 'updated_at')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment,
                    DraggableMPTTAdmin,
                    list_display=(
                        'tree_actions',
                        'indented_title',
                        'id',
                        'level',
                        'text',
                    ),
                    list_display_links=(
                        'indented_title',
                    ))



