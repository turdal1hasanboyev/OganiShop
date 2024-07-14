from django import forms
from ckeditor.widgets import CKEditorWidget
from apps.blog.models import Blog


class BlogAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = '__all__'
        