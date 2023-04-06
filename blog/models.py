from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from pytils.translit import slugify

class Category(models.Model):
    name = models.CharField('category', max_length=20)
    slug = models.SlugField()
    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField('tag', max_length=20)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class Post(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    text = models.TextField(max_length=2000)
    category = models.ForeignKey(Category, 
        on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    published = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, 
        related_name='post_likes', blank=True)
    bookmarks = models.ManyToManyField(User, 
        related_name='bookmarks', blank=True)

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f'{self.owner} {self.title}'

    def number_of_likes(self):
        if self.likes.count() == 0:
            return ''
        else:
            return self.likes.count()

    def number_of_bookmarks(self):
        if self.bookmarks.count() == 0:
            return ''
        else:
            return self.bookmarks.count()
    
    def number_of_comments(self):
        if self.comments.count() == 0:
            return ''
        else:
            return self.comments.filter(approved=True).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, 
        on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-published']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text