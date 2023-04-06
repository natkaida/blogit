from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Interest, Message
from django.forms import ModelForm, FileInput


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 
        'password1', 'password2']
        labels = {
            'first_name': 'Имя и фамилия',
            'email': 'Email', 
            'username':'Логин', 
            'password1':'Пароль', 
            'password2': 'Подтверждение пароля'

        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username',
                  'summary', 'about', 'image', 
                  'city', 'profession',
                  'github', 'linkedin', 'twitter',
                  'youtube']
        labels = {
            'name': 'Имя и фамилия',
            'email': 'Email', 
            'username':'Логин',
            'city': 'Город', 
            'profession': 'Профессия',
            'summary': 'В двух словах о себе',
            'about': 'Подробнее о себе',
            'image': 'Изменить фото профиля',
        }
        widgets = {
            'image': FileInput(),
        }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})
                

class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = '__all__'
        exclude = ['profile', 'slug']

        labels = {
            'name': 'Название',
            'description':'Описание',
          
        }

    def __init__(self, *args, **kwargs):
        super(InterestForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})




class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        labels = {'name': 'Имя и фамилия',
            'email': 'Email', 
            'subject':'Тема сообщения',
            'body':'Текст сообщения'
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})
