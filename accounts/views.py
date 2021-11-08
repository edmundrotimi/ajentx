from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from profiles.models import Profile
from .utility_function import user_request


User = get_user_model()


class AccountSuspension(LoginRequiredMixin, TemplateView):
    template_name = 'account/suspension.html'


class AccountSignIn(View):

    def dispatch(self, request, *args, **kwargs):
        # check if user is logined in
        if self.request.user.is_authenticated:
            # get profile
            profile = Profile.objects.filter(
                user=request.user).values_list('slug', flat=True)
            return HttpResponseRedirect(f'/account/profile/{profile[0]}/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        template = 'account/signin.html'
        return render(request, template)

    def post(self, request):

        if request.POST.get('role') == 'user':

            username = request.POST['username']
            password = request.POST['password']

            # Authenticate user first
            user = authenticate(
                request, username=username, password=password)
            if user == None:
                messages.error(request, 'Invalid username and password')
                return redirect('signin')
            else:
                # login user
                login(request, user)

                # profile
                profile = Profile.objects.filter(
                    user=request.user).values_list('slug', flat=True)

                # redirect
                return HttpResponseRedirect(f'/account/profile/{profile[0]}/')
        else:
            user_request(request)
            return HttpResponseRedirect('/accounts/login/')


class AccountSignUp(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'account/signup.html'
    success_url = reverse_lazy('profile_create')
    success_message = 'Account created successfully'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if form.cleaned_data('role') == 'user':
                super().post(request, *args, **kwargs)
                return HttpResponseRedirect(self.get_success_url())
            else:
                user_request(request)

    def dispatch(self, request, *args, **kwargs):
        # check if user is logined in
        if self.request.user.is_authenticated:
            # get profile
            profile = Profile.objects.filter(
                user=request.user).values_list('slug', flat=True)
            return HttpResponseRedirect(f'/account/profile/{profile[0]}/')
        return super().dispatch(request, *args, **kwargs)
