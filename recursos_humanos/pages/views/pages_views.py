from http import HTTPStatus

from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse

from ..forms import LoginForm


class HomeView(View):

    template_name = 'pages/home.html'

    def get(self, request):

        return render(request, self.template_name, {})


class LoginView(View):

    template_name = 'pages/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('pages_app:home')

    def get(self, request):

        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        """
        This method validates the login form.
        """
        form = self.form_class(request.POST)

        is_valid = form.is_valid()
        if not is_valid:
            return HttpResponse(content='Error, invalid form', status=HTTPStatus.BAD_REQUEST)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse(content='Error, user not found', status=HTTPStatus.NOT_FOUND)

        login(request, user)

        return JsonResponse(data={'redirect_url': self.success_url}, status=HTTPStatus.FOUND)
