from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Q
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from blog.models import BlogComment
from profiles.models import Profile
from .models import PropertyListings
from .forms import ListingsForms, TourForm, AgentContactForm


class CreateListings(LoginRequiredMixin, generic.CreateView):
    form_class = ListingsForms
    model = PropertyListings
    template_name = 'listings/create-listing.html'
    success_url = '/'

    def get_profile(self):
        return Profile.objects.get(user=self.request.user)

    def get_listing(self):
        return PropertyListings.objects.get(user=self.get_profile().id)

    def get_success_url(self):
        return reverse_lazy('update_detail_listings', args=(self.get_listing().slug,))

    def form_valid(self, form):
        form.instance.user = self.get_profile()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/create/profile/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
            elif Profile.objects.filter(user=self.request.user, status='Buyer'):
                return HttpResponsePermanentRedirect('/listings/error/')
        return super().dispatch(request, *args, **kwargs)


class UpdateListings(LoginRequiredMixin, generic.UpdateView):
    form_class = ListingsForms
    model = PropertyListings
    queryset = PropertyListings.objects.filter(publish=True)
    template_name = 'listings/update-listing.html'
    success_url = ''

    def get_profile(self):
        return Profile.objects.get(user=self.request.user)

    def get_listing(self):
        return PropertyListings.objects.get(user=self.get_profile().id)

    def get_queryset(self):
        return PropertyListings.objects.filter(user__user=self.request.user, slug=self.kwargs.get('slug'))

    def get_success_url(self):
        listing_slug = self.get_listing().slug
        return reverse_lazy('update_detail_listings', args=(listing_slug,))

    def form_valid(self, form):
        form.instance.user = self.get_profile()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/create/profile/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
            elif Profile.objects.filter(user=self.request.user, status='Buyer'):
                return HttpResponsePermanentRedirect('/listings/error/')
        return super().dispatch(request, *args, **kwargs)


class ListingsUpdateDetails(LoginRequiredMixin, generic.DetailView):
    model = PropertyListings
    queryset = PropertyListings.objects.filter(publish=True)
    template_name = 'listings/update-details-listing.html'
    context_object_name = 'listing'

    def get_queryset(self):
        return PropertyListings.objects.filter(user__user=self.request.user, slug=self.kwargs.get('slug'))

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/create/profile/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
            elif Profile.objects.filter(user=self.request.user, status='Buyer'):
                return HttpResponsePermanentRedirect('/listings/error/')
        return super().dispatch(request, *args, **kwargs)


class ListingsError(LoginRequiredMixin, generic.TemplateView):
    template_name = 'listings/create_error.html'


class DeleteListing(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = PropertyListings
    success_url = reverse_lazy('listings')
    template_name = 'listings/listing-delete.html'
    success_message = 'Lisitng Deleted Successfully'

    def get_queryset(self):
        return PropertyListings.objects.filter(user__user=self.request.user, slug=self.kwargs.get('slug'))

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/create/profile/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
            elif Profile.objects.filter(user=self.request.user, status='Buyer'):
                return HttpResponsePermanentRedirect('/listings/error/')
        return super().dispatch(request, *args, **kwargs)


class Listings(LoginRequiredMixin, generic.ListView):
    model = PropertyListings
    queryset = PropertyListings.objects.filter(publish=True)
    template_name = 'listings/property-grid.html'
    context_object_name = 'listings'
    paginate_by = 6

    def get_queryset(self):
        # for search
        status = self.request.GET.get('status', 'empty')
        state = self.request.GET.get('state', 'empty')
        city = self.request.GET.get('city', 'empty')
        amenities = self.request.GET.get('amenities', 'empty')
        price = self.request.GET.get('price', 'empty')

        query = PropertyListings.objects.annotate(
            search=SearchVector('property_status', 'state', 'city', 'amenities', 'property_price'),).filter(
            Q(search=status) | Q(search__icontains=state) | Q(search__icontains=city) | Q(search__icontains=amenities) | Q(search__gte=price) & Q(publish=True))

        if not bool(query):
            query = super().get_queryset()

        # setion for sort filtering
        sort = self.request.GET.get('sort', None)
        if sort != None:
            query = PropertyListings.objects.annotate(
                search=SearchVector('user__status'),).filter(Q(search=sort) & Q(publish=True))

            if sort == "Newest":
                query = super().get_queryset()

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_listings'] = PropertyListings.objects.filter(publish=True)
        return context

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/create/profile/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        return super().dispatch(request, *args, **kwargs)


class ListingDetails(LoginRequiredMixin, generic.DetailView):
    model = PropertyListings
    queryset = PropertyListings.objects.filter(publish=True)
    template_name = 'listings/property-details.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listings"] = PropertyListings.objects.filter(publish=True)
        context['form'] = ''
        return context

    def post(self, request, *args, **kwargs):
        listing_uploder = PropertyListings.objects.get(
            publish=True, slug=self.kwargs.get('slug'))

        if request.POST.get('form-type') == 'tour':
            form = TourForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                clean_form = form.cleaned_data
                form.save()

                mail = EmailMessage(
                    subject="New Tour Request",
                    body=render_to_string('email/email.html', {
                        'subject': 'New User Message',
                        'fullname': clean_form['full_name'],
                        'email': clean_form['email'][:3]+'...',
                        'phone_number': clean_form['phone_number'],
                        'message': clean_form['message']
                    }),
                    from_email='AjentX <noreply@ajentx.com>',
                    to=[listing_uploder.user.user.email, ],
                )

                mail.send()

                messages.success(request, "Message Sent to Agent")

                return redirect(f'{request.get_full_path()}')

            else:
                messages.error(request, "Invalid for form fields!")
                return redirect(f'{request.get_full_path()}')

        else:
            form = AgentContactForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                clean_form = form.cleaned_data
                form.save()

                mail = EmailMessage(
                    subject="New Listing Message",
                    body=render_to_string('email/email.html', {
                        'subject': 'New User Message',
                        'fullname': clean_form['contact_full_name'],
                        'email': clean_form['contact_email'][:3]+'...',
                        'phone_number': clean_form['contact_phone_number'],
                        'message': clean_form['contact_message']
                    }),
                    from_email='AjentX <noreply@ajentx.com>',
                    to=[listing_uploder.user.user.email, ],
                )

                mail.send()

                messages.success(request, "Message Sent to Agent")

                return redirect(f'{request.get_full_path()}')
            else:
                messages.error(request, "Invalid for form fields!")
                return redirect(f'{request.get_full_path()}')

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/account/create/profile/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        return super().dispatch(request, *args, **kwargs)
