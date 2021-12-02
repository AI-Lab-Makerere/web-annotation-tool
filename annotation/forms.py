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


class AnnotatorModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnnotatorModelForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].required = True

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username',
        ]


class AssignAnnotatorForm(forms.Form):
    annotator = forms.ModelChoiceField(queryset=Annotator.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        annotators = Annotator.objects.filter(leader=request.user.leader)
        super(AssignAnnotatorForm, self).__init__(*args, **kwargs)
        self.fields["annotator"].queryset = annotators
