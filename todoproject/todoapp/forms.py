from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['description']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What do you need to do?',
                'aria-label': 'Task description',
            }),
        }
        labels = {
            'description': 'Task Description',
        }