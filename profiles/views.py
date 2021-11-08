from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView,  DetailView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

from profiles.models import Profile
from .forms import ProfileForm

User = get_user_model()


class CreateProfile(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = ProfileForm
    model = Profile
    template_name = 'account/profile.html'
    success_url = reverse_lazy('/account/profile/')
    success_message = 'Profile created successfully'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # info: get user instance
        user = User.objects.get(username=self.request.user)
        # update user first and last name
        user.first_name = form.instance.first_name
        user.last_name = form.instance.last_name
        user.save()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        profile = Profile.objects.filter(
            user=self.request.user).values_list('slug', flat=True)
        return reverse_lazy('profile_update', args=(profile[0],))

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect(self.get_success_url())
        else:
            return super().dispatch(request, *args, **kwargs)


class ProfileDetail(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Profile
    querySet = Profile.objects.all()
    context_object_name = 'profile'
    template_name = 'account/profile-detail.html'
    success_message = 'Pofile Updated Successfully'
    success_url = '/account/profile/%(slug)'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponseRedirect('/account/profile/create/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponsePermanentRedirect('/accounts/login/')


class UpdateProfile(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = Profile
    success_url = '/account/profile/%(slug)'
    template_name = 'account/profile-update.html'
    success_message = 'Pofile Updated Successfully'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # info: get user instance
        user = User.objects.get(username=self.request.user)
        # update user first and last name
        user.first_name = form.instance.first_name
        user.last_name = form.instance.last_name
        user.save()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        profile = Profile.objects.filter(
            user=self.request.user).values_list('slug', flat=True)
        return reverse_lazy('profile_update', args=(profile[0],))

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponseRedirect('/account/profile/create/')
            elif Profile.objects.filter(Q(user=self.request.user) & Q(publish=False)):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponsePermanentRedirect('/accounts/login/')


class DeleteProfile(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Profile
    success_url = reverse_lazy('home')
    template_name = 'account/profile-delete.html'
    success_message = 'Pofile Updated Successfully'

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponseRedirect('/account/profile/create/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        else:
            return super().dispatch(request, *args, **kwargs)
