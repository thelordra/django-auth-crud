from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "important"]
        # complementos para estilizar el formulario
        # Se inyectan estilos de Boostrap al formulario en forma de diccionarios
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe la tarea'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }
