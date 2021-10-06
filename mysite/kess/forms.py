from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Kess

from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2', )


class CreateKessForm(ModelForm):
    emoji = forms.CharField(widget=EmojiPickerTextareaAdmin)

    class Meta:
        model = Kess
        fields = ['emoji', 'reponse', 'category']


class UserAvatarForm(forms.Form):

    avatar = forms.CharField(widget=EmojiPickerTextInputAdmin)
