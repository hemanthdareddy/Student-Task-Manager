from django import forms
from .models import Task, Subject

class TaskForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=False)
    class Meta:
        model = Task
        fields = ['title', 'subject', 'description', 'due_date', 'due_time']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)