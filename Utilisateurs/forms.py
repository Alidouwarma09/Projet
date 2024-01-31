# Utilisateurs/forms.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ClearableFileInput

from .models import CustomUser, BlogPost
from django import forms


class UserRegistrationForm(UserCreationForm):
    photo = forms.ImageField(required=False)
    username = forms.CharField(max_length=15, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=False, widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'nom', 'prenom', 'photo', 'password1', 'password2', 'role']

        def clean(self):
            cleaned_data = super().clean()

            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 and password2 and password1 != password2:
                self.add_error('password2', "Les deux mots de passe ne correspondent pas.")

            return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom'})
        self.fields['prenom'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Prénom'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirmez le mot de passe'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Numéro de téléphone'})


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=15, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']


class ActivateUserForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())


class DeactivateUserForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
