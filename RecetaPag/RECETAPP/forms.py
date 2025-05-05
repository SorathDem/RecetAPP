from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Receta
from .models import comentario

class CustomUserCreationForm(forms.ModelForm):  # Se usa ModelForm en lugar de UserCreationForm
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith('@ucundinamarca.edu.co'):
            raise ValidationError("Solo se permiten correos @ucundinamarca.edu.co")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not password1:
            raise forms.ValidationError("Este campo es obligatorio.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Guarda la contraseña correctamente
        if commit:
            user.save()
        return user

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'imagen', 'ingredientes', 'pasos', 'video']
        widgets = {
            'ingredientes': forms.Textarea(attrs={'rows': 4}),
            'pasos': forms.Textarea(attrs={'rows': 6}),
        }
    
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = comentario
        fields = ['texto', 'calificacion']
        widgets = {
            'texto': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario...'}),
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }