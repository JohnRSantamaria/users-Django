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


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña actual"
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña nueva"
            }
        )
    )


class VerificationForm(forms.Form):
    code_registro = forms.CharField(required=True)

    # esta funcion se ejecuta en el momento que se inicializa este fromulario
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_code_registro(self):
        codigo = self.cleaned_data['code_registro']

        if len(codigo) == 6:
            # Verificamos si el codigo y el id de usuario son valido
            activo = User.objects.code_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('El codigo es incorrecto')
        else:
            raise forms.ValidationError('El codigo es incorrecto')
