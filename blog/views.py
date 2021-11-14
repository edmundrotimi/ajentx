from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.models import Profile
from .models import BlogComment, BlogPost


class BlogList(LoginRequiredMixin, generic.ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(publish=True)
    context_object_name = 'posts'
    template_name = 'blog/blog-list.html'
    paginate_by = 4

    def get_queryset(self):
        search_field = self.request.GET.get('search_field', 'empty')

        query = BlogPost.objects.annotate(
            search=SearchVector('title', 'detail', 'category', 'tags'),).filter(
                Q(search__icontains=search_field))

        if search_field == 'empty':
            if not bool(query):
                query = super().get_queryset()

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["counter_cat_hom"] = BlogPost.objects.filter(
            category='Home improvement').count()
        context["counter_cat_arch"] = BlogPost.objects.filter(
            category='Architecture').count()
        context["counter_cat_tip"] = BlogPost.objects.filter(
            category='Tips and advice').count()
        context["counter_cat_int"] = BlogPost.objects.filter(
            category='Interior').count()
        context["counter_cat_est"] = BlogPost.objects.filter(
            category='Real Estate').count()

        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/accounts/suspension/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        return super().dispatch(request, *args, **kwargs)


class BlogDetail(LoginRequiredMixin, generic.DetailView):
    model = BlogPost
    context_object_name = 'post'
    template_name = 'blog/blog-details.html'

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        post = BlogPost.objects.get(slug=self.kwargs.get('slug'))

        full_name = request.POST.get('name')
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST.get('message')
        try:

            comment = BlogComment(
                user= profile,
                post = post,
                full_name=full_name,
                email=email,
                subject=subject,
                message=message
            )

            comment_check = comment.clean_fields()
            comment.save()

            messages.error(request, 'Message sent.')

            return HttpResponseRedirect(f"{request.get_full_path()}")

        except ValidationError as e:
            string_error = ''
            for key, value in e:
                for i in value:
                    string_error = string_error + i
            
            messages.error(request, f'Error: {string_error}')

            return HttpResponseRedirect(f"{request.get_full_path()}")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = BlogComment.objects.filter(publish=True)
        context['all_post'] = BlogPost.objects.filter(publish=True)
        context["counter_cat_hom"] = BlogPost.objects.filter(
            category='Home improvement').count()
        context["counter_cat_arch"] = BlogPost.objects.filter(
            category='Architecture').count()
        context["counter_cat_tip"] = BlogPost.objects.filter(
            category='Tips and advice').count()
        context["counter_cat_int"] = BlogPost.objects.filter(
            category='Interior').count()
        context["counter_cat_est"] = BlogPost.objects.filter(
            category='Real Estate').count()
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not Profile.objects.filter(user=self.request.user).exists():
                return HttpResponsePermanentRedirect('/accounts/suspension/')
            elif Profile.objects.filter(user=self.request.user, publish=False):
                return HttpResponsePermanentRedirect('/accounts/suspension/')
        return super().dispatch(request, *args, **kwargs)
