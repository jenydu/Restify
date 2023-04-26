from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from django.views import View

from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView

from django.contrib.auth import login, logout

from .forms import RegisterForm, LoginForm, UpdateProfileForm, GetProfileForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


###
class AuthenticatedView:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        return super().dispatch(request, *args, **kwargs)
###
 
class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class= RegisterForm
    success_url = reverse_lazy('accounts:login')
    def form_valid(self, form):
        self.request.session['from'] = 'signup'
        
        return super().form_valid(form)
    
class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/accounts/profile/view/'
    
    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)

    
class LogoutView(View):
    success_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect(self.success_url)
        else:
            return HttpResponse('OK', status=200)


class ProfileViewView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return JsonResponse(data)
    


#####################
class ProfileEditView(AuthenticatedView, View):
    template_name = 'accounts/profile.html'
    success_url = '/accounts/profile/view/'
    form_class= UpdateProfileForm
    def get(self, request, *args, **kwargs):
        user = request.user
        form_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        form = GetProfileForm(form_data)
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):

        user = request.user
        form_data = {
            'first_name': request.POST.get('first_name',''),
            'last_name': request.POST.get('last_name',''),
            'email': request.POST.get('email',''),
            'password1' : request.POST.get('password1',''),
            'password2' : request.POST.get('password2',''),
        }
        form = UpdateProfileForm(form_data)
        if form.is_valid():
            if form_data['first_name'] != user.first_name:
                user.first_name = form_data['first_name']
                user.save()
            if form_data['last_name'] != user.last_name:
                user.last_name = form_data['last_name']
                user.save()
            if form_data['email'] != user.email:
                user.email = form_data['email']
                user.save()
            if form_data['password1']:
                if form_data['password1'] != form_data['password2']:
                    user.set_password(form_data['password1'])
                    user.save()

            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form, 'form_data': form_data})