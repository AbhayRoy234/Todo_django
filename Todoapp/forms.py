from django.forms import ModelForm #inporting model form
from .models import Todo

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']