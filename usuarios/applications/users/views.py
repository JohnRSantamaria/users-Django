from django.views.generic.edit import View
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout


from .models import User
from .functions import code_generator
from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm
)

# Create your views here.


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = "/"

    def form_valid(self, form):
        # Generamos el codigo
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            # cada vez que se cree un usuario nuevo se generara un codigo aleatorio de 6 digitos
            code_registro=codigo
        )
        # Enviar codigo al email del user
        asunto = 'Confirmacion de email'
        mensaje = 'Codigo de verificacion: ' + codigo
        email_remitente = 'santamariajohnd@gmail.com'
        #
        send_mail(asunto, mensaje, email_remitente,
                  [form.cleaned_data['email'],])
        # Redirigir a una pantalla de validación
        # Enviar el id del usuario cuando se registre correctamente por parametros
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk': usuario.id}
            )
        )


class LoginUser(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    # Recordar poner el url en caso de que no este logeado
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        # Recuperando el usuario que esta activo actualmente
        # esto se puede hacer desde cualquier lugar para obtener el usuario activo
        usuario = self.request.user

        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )
        # Si el usuario esta autenticado
        if user:
            # obtejemos el password de el formulario
            new_password = form.cleaned_data['password2']
            # recordar que esto guarda la contraseña encriptandola
            usuario.set_password(new_password)
            # NO olvida guardar
            usuario.save()
        # despues de actulizarla sacarlo para que la actulice
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class CodeVerificationView(FormView):
    template_name = "users/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy("user_app:user-login")

    # le decimos que envie nuevos kwords hacia el formulario con el que estamos trabajando
    # en este caso VerificationForm
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
        ''' 
            objects.get = este no tiene la funcion update
            objects.filter  = esta es una forma mucho mas obtima de actualizarlo    
        '''
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )

        return super(CodeVerificationView, self).form_valid(form)
