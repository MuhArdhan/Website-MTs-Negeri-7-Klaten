from django import forms
from home.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'publish', 'status', 'category', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title',}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter slug'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'publish': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'readonly': 'readonly'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)  # Pop the user from kwargs
            super().__init__(*args, **kwargs)
            if self.user:
                self.fields['author'].queryset = User.objects.filter(id=self.user.id)  # Limit queryset to logged-in user
                self.fields['author'].initial = self.user  # Pre-set the author field
                self.fields['author'].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})