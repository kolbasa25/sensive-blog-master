from django.contrib import admin
from blog.models import Post, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'likes', 'tags')
    list_display = ('title', 'author', 'published_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'post')
    list_display = ('text_preview', 'author', 'post', 'published_at')

    def text_preview(self, obj):
        return obj.text[:50] + '…' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст комментария'