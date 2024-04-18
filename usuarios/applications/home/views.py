import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
# Create your views here.


class FechaMixin(object):
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context["fecha"] = datetime.datetime.now()

        return context


class HomePage(LoginRequiredMixin, FechaMixin, TemplateView):
    template_name = "home/index.html"
    # Adonde se va enviar cuando no esta logeado
    login_url = reverse_lazy('users_app:user-login')


class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
