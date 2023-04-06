from django.forms import ModelForm
from django import forms
from .models import Post, Comment, Category

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 
        'tags', 'text']
        labels = {
            'title': 'Название',
            'category':'Категория',
            'tags':'Теги', 
            'text':'Текст',
            }

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
        category = forms.ModelChoiceField(queryset=Category.objects.none(), 
            empty_label="(Работа)")
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})    
        self.fields['category'].empty_label = None
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        labels = {
            'text': 'Ваш комментарий'
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'}) 