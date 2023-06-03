from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing, name='landing'),
    path('profiles/', views.profiles, name='profiles'),
    path('landing/', views.landingLogin, name='landingLogin'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),   
    path('profile/<str:username>/', views.userProfile, 
        name='user-profile'),
    path('follow/<str:username>/', views.follow_unfollow, 
        name='follow-unfollow'),
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, 
        name='edit-account'),
    path('create-interest/', views.createInterest, 
        name='create-interest'),
    path('update-interest/<slug:interest_slug>/', 
        views.updateInterest, name='update-interest'),
    path('delete-interest/<slug:interest_slug>/', 
        views.deleteInterest, name='delete-interest'),
    path('interest/<slug:interest_slug>', 
        views.profiles_by_interest, name='interest'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.viewMessage, name='message'),
    path('create-message/<str:username>/', 
        views.createMessage, name='create-message'),

]