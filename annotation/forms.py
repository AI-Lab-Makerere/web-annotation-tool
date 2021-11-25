from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class TeamLeaderModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TeamLeaderModelForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].required = True
        self.fields['category'].required = True

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username',
            'category',
        ]


class BatchModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BatchModelForm, self).__init__(*args, **kwargs)
        self.fields['batch_name'].required = True
        self.fields['batch_file'].required = True

    class Meta:
        model = Batch
        fields = [
            'batch_name',
            'batch_file',
        ]
