from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'placeholder': 'dd/mm/yyyy'
        }),
        input_formats=['%d/%m/%Y'],
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'group', 'due_date', 'completed']
