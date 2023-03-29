from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile, Interest
from .forms import CustomUserCreationForm, ProfileForm, InterestForm, MessageForm
from .utils import paginateObjects, searchProfiles
from django.db.models import Q

def landing(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateObjects(request, 
        profiles, 3)
    context = {'profiles': profiles, 
    'search_query': search_query,
    'custom_range': custom_range}

    return render(request, 'landing.html', context)


def landingLogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 
                'Такого пользователя нет в системе')
        user = authenticate(request, username=username, 
            password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' 
                in request.GET else 'account')
        else:
            messages.error(request, 
                'Неверное имя пользователя или пароль')
    return redirect('landing')

def contact(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        body = request.POST['body']
   
        msg = f'Пользователь {name} с email {email} сообщает:\n'
        msg += f'\n{subject}\n\n'
        msg += f'{body}'
        try: 
            if name and email and subject and body != '':
                send_mail(
                    subject=subject,
                    message=msg,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.RECIPIENT_ADDRESS]
                )
                messages.success(request, 
                    'Сообщение отправлено! Мы скоро ответим.')
               
            else:
                messages.error(request, 
                    'Заполните, пожалуйста, все поля контактной формы.')
        except:
            messages.error(request, 
                'Сервер посчитал сообщение спамом. Попробуйте позже.')

    return redirect('landing')


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateObjects(request, 
        profiles, 3)
    context = {'profiles': profiles, 
    'search_query': search_query,
    'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 
                'Такого пользователя нет в системе')

        user = authenticate(request, 
            username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' 
                in request.GET else 'account')

        else:
            messages.error(request, 
                'Неверное имя пользователя или пароль')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 
                'Аккаунт успешно создан!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request, 
                'Во время регистрации возникла ошибка')

    context = {'page': page, 'form': form}
    return render(request, 
        'users/login_register.html', context)


def userProfile(request, username):
    profile = Profile.objects.get(username=username)
    interests = profile.interest_set.all()
    profiles = profile.follows.all()

    custom_range, profiles = paginateObjects(request, 
        profiles, 3)
    
    context = {'profile': profile, 'profiles': profiles,
               'interests': interests,
               'custom_range': custom_range}

    return render(request, 
        'users/user-profile.html', context)

@login_required 
def profiles_by_interest(request, interest_slug):
    interest = Interest.objects.filter(slug__icontains=interest_slug)
    profiles = Profile.objects.exclude(user=request.user).distinct().filter(
        Q(interest__in=interest))
    context = {'profiles': profiles}

    return render(request, 'users/profiles.html', context)

@login_required
def userAccount(request):
    profile = request.user.profile
    interests = profile.interest_set.all()
    profiles = profile.follows.all()
    custom_range, profiles = paginateObjects(request, 
        profiles, 3)

    context = {'profile': profile, 'profiles': profiles,
    'interests': interests, 'custom_range': custom_range}
    return render(request, 'users/account.html', context)



@login_required
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, 
            instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form': form}
 
    return render(request, 
        'users/profile_form.html', context)


@login_required
def createInterest(request):
    profile = request.user.profile
    form = InterestForm()

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest_slug = request.POST.get('slug')
            interest_description = request.POST.get('description')
            profile.interest_set.get_or_create(name=interest, slug=interest_slug, description=interest_description, profile=profile)
            messages.success(request, 'Интерес добавлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 
        'users/interest_form.html', context)


@login_required
def updateInterest(request, interest_slug):
    profile = request.user.profile
    interest = profile.interest_set.get(slug=interest_slug)
    form = InterestForm(instance=interest)

    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            messages.success(request, 
                'Интерес успешно обновлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 
        'users/interest_form.html', context)


@login_required
def deleteInterest(request, interest_slug):
    profile = request.user.profile
    interest = profile.interest_set.get(slug=interest_slug)
    if request.method == 'POST':
        interest.delete()
        messages.success(request, 'Интерес успешно удален')
        return redirect('account')

    context = {'object': interest}
    return render(request, 'delete_template.html', context)


@login_required
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 
    'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read is False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)



def createMessage(request, username):
    recipient = Profile.objects.get(username=username)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 
                'Сообщение успешно отправлено!')
            return redirect('user-profile', 
                username=recipient.username)

    context = {'recipient': recipient, 'form': form}
    return render(request, 
        'users/message_form.html', context)    

@login_required
def follow_unfollow(request, username):
    profile = Profile.objects.get(username=username)
    if request.method == 'POST':
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get('follow')
        if action == 'follow':
            current_user_profile.follows.add(profile)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))