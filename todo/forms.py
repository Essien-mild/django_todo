
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
        }),
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'priority', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter description',
                'rows': 2,   # keeps textarea small
                'style': 'min-height:40px;'
            }),
            'priority': forms.Select(),
        }
