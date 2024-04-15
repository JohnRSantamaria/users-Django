from django import forms
from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña"
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repetir contraseña"
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero'
        )

    def clean_password2(self,):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'las constaseñas no son las mismas')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "style": "{margin: 10px}"
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña"
            }
        )
    )

    """ Validación del formulario
        Cuando se requiera validar todos los datos del formulario 
        y no solo uno podremos poner solamente clean        
    """

    def clean(self):

        # cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(
            username=username,
            password=password
        ):
            raise forms.ValidationError(
                'Los datos de usuario no son correctos')

        # return self.cleaned_data
        # return super().clean()
