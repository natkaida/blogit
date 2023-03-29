from django.contrib import admin
from .models import Post, Category, Tag, Comment

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Post)
