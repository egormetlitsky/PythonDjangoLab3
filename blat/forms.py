__author__ = 'admin-pc'
from django import forms


class LikeForm(forms.Form):
    blat_id = forms.IntegerField()
    action = forms.CharField()
