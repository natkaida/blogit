from django.contrib.auth.models import User
from django.db import models
from pytils.translit import slugify



class Profile(models.Model):
    user = models.OneToOneField(User, 
        on_delete=models.CASCADE)
    name = models.CharField(max_length=50, 
        blank=True, null=True)
    email = models.EmailField(max_length=50, 
        blank=True, null=True)
    username = models.CharField(max_length=50, 
        blank=True, null=True)
    summary = models.CharField(max_length=100, 
        blank=True, null=True)
    city = models.CharField(max_length=20, 
        blank=True, null=True)
    profession = models.CharField(max_length=50, 
        blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(
        null=True, blank=True, upload_to='profile_images', 
        default='profile_images/default.jpg')
    github = models.CharField(max_length=100,  
        default='https://github.com')
    twitter = models.CharField(max_length=100, 
        default='https://twitter.com')
    linkedin = models.CharField(max_length=100, 
        default='https://linkedin.com')
    youtube = models.CharField(max_length=100, 
        default='https://youtube.com')
    website = models.CharField(max_length=100, 
        default='https://mysite.com')
    created = models.DateTimeField(auto_now_add=True)
    follows = models.ManyToManyField(
        'self', related_name='followed_by', 
        symmetrical=False, blank=True
    )

    class Meta:
        ordering = ['created']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

class Interest(models.Model):
    name = models.CharField(max_length=50, 
        blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(
        Profile, null=True, blank=True, 
        on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'
        unique_together = ('name', 'slug', 'profile')

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, 
        null=True, blank=True)
    recipient = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, 
        null=True, blank=True)
    email = models.EmailField(max_length=200, 
        null=True, blank=True)
    subject = models.CharField(max_length=200, 
        null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'