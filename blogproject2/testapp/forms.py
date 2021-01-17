from django import forms
from testapp.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')
