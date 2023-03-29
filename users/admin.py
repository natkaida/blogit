from django.contrib import admin
from .models import Profile, Interest, Message
class InterestInline(admin.TabularInline):
    model = Interest
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    inlines = [InterestInline]


admin.site.register(Message)
admin.site.register(Interest)
admin.site.register(Profile, ProfileAdmin)