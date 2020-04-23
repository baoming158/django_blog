from django import forms
from .models import AriticlePost


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = AriticlePost
        fields = ('title', 'body', 'tags', 'avatar')
