from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),    
    path('', include('users.urls')),
    path('', include('polls.urls')),
    path('', include('quizzes.urls')),
]

urlpatterns += static(settings.MEDIA_URL, 
	document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, 
	document_root=settings.STATIC_ROOT)