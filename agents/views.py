from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail.message import EmailMessage
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.contrib.postgres.search import SearchVector
from blog.models import BlogComment
from listings.forms import AgentContactForm
from profiles.models import Profile, AgentContact
from listings.models import PropertyListings


class Agentlist(LoginRequiredMixin, ListView):
    model = Profile
    queryset = Profile.objects.filter(publish=True)
    template_name = 'agent/agents-grid.html'
    context_object_name = 'agent'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agent_count_seller'] = Profile.objects.filter(
            publish=True, status='Seller').count()
        context['agent_count_realtor'] = Profile.objects.filter(
            publish=True, status='Broker/Realtor').count()
        context['listings'] = PropertyListings.objects.filter(
            Q(publish=True))
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/profile/create/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        return super().dispatch(request, *args, **kwargs)


class AgentSearch(LoginRequiredMixin, ListView):
    model = Profile
    queryset = Profile.objects.filter(publish=True)
    template_name = 'agent/agents-search.html'
    context_object_name = 'agent'
    paginate_by = 6

    def get_queryset(self):
        agent_name = self.request.GET.get('name', 'empty')
        category = self.request.GET.get('category', 'empty')
        city = self.request.GET.get('city', 'empty')

        query = Profile.objects.annotate(
            search=SearchVector('first_name', 'last_name', 'city', 'status'),).filter(
            Q(search=agent_name) | Q(search=category) | Q(search=city) & Q(publish=True) & ~Q(status='Buyer'))

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agent_count_seller'] = Profile.objects.filter(
            publish=True, status='Seller').count()
        context['agent_count_realtor'] = Profile.objects.filter(
            publish=True, status='Broker/Realtor').count()
        context['listings'] = PropertyListings.objects.filter(publish=True)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/profile/create/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        return super().dispatch(request, *args, **kwargs)


class AgentSearchSort(LoginRequiredMixin, ListView):
    model = Profile
    queryset = Profile.objects.filter(publish=True)
    template_name = 'agent/agents-sort.html'
    context_object_name = 'agent'
    paginate_by = 6

    def get_queryset(self):
        sort = self.request.GET.get('sort')

        query = Profile.objects.annotate(
            search=SearchVector('status'),).filter(Q(search=sort) & Q(publish=True) & ~Q(status='Buyer'))
        if sort == "Newest":
            query = Profile.objects.filter(
                Q(publish=True) & ~Q(status='Buyer'))
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agent_count_seller'] = Profile.objects.filter(
            publish=True, status='Seller').count()
        context['agent_count_realtor'] = Profile.objects.filter(
            publish=True, status='Broker/Realtor').count()
        context['listings'] = PropertyListings.objects.filter(publish=True)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/profile/create/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        return super().dispatch(request, *args, **kwargs)


class AgentDetails(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'agent/agents-details.html'
    context_object_name = 'agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = PropertyListings.objects.filter(publish=True)
        context['sales_count'] = PropertyListings.objects.filter(
            property_status='Sale').count()
        context['lease_count'] = PropertyListings.objects.filter(
            property_status='Lease').count()
        context['rent_count'] = PropertyListings.objects.filter(
            property_status='Rent').count()
        context['sold_count'] = PropertyListings.objects.filter(
            property_status='Sold Out').count()
        return context

    def post(self, request, *args, **kwargs):
        agent = Profile.objects.get(
            publish=True, slug__startswith=self.kwargs.get('slug'))

        contact_full_name = request.POST['contact_full_name']
        contact_email = request.POST['contact_email']
        contact_phone_number = request.POST['contact_phone_number']
        contact_message = request.POST['contact_message']

        contact = AgentContact(user=request.user, contact_full_name=contact_full_name,
                               contact_email=contact_email, contact_phone_number=contact_phone_number,
                               contact_message=contact_message)
        try:

            form_validity = contact.clean_fields()
            contact.save()

            mail = EmailMessage(
                subject="New Listing Message",
                body=render_to_string('email/email.html', {
                    'subject': 'New User Message',
                    'fullname': contact_full_name,
                    'email': contact_email[:3]+'...',
                    'phone_number': contact_phone_number,
                    'message': contact_message
                }),
                from_email='AjentX <noreply@ajentx.com>',
                to=[agent.user, ],
            )

            mail.send()

            messages.success(request, "Message Sent to Agent")

            return redirect(f'{request.get_full_path()}')

        except ValidationError as e:
            string_error = ''
            for key, value in e:
                for i in value:
                    if 'Ensure this value has at least 10 characters' in i:
                        string_error = string_error + 'Message: '+i
                    else:
                        string_error = string_error + i
            messages.error(request, f'Error- \n {string_error}')

            return redirect(f'{request.get_full_path()}')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/profile/create/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        return super().dispatch(request, *args, **kwargs)
