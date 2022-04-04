from .models import Article
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')


class NewUserForm(UserCreationForm):
    email =forms.EmailField(required=True)

    class Meta:
        model =User
        fields =("username","email","password1","password2") 

        def save(self,commit=True):
            user =super(NewUserForm,self).save(commit=False)
            user.email =self.cleaned_data['email']
            if commit:
                user.save()
            return user  

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['editor', 'pub_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }                 