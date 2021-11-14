from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import generic
from contact.models import UserContact
from listings.models import PropertyListings
from blog.models import BlogComment, BlogPost
from profiles.models import Profile


class HomeView(generic.TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listings"] = PropertyListings.objects.order_by(
            '-last_updated').filter(publish=True)
        context["agents"] = Profile.objects.order_by(
            '-last_updated').filter(publish=True)
        context["blog"] = BlogPost.objects.order_by(
            '-last_updated').filter(publish=True)[:3]
        return context


class ServiceView(generic.TemplateView):
    template_name = 'pages/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listings"] = PropertyListings.objects.order_by(
            '-last_updated').filter(publish=True)[:3]
        return context


class Faq(generic.View):
    template_name = 'pages/faq.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        fullname = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        subject = 'User FAQ',

        try:

            model_instance = UserContact(
                fullname=fullname,
                email=email,
                subject=subject,
                message=message
            )

            model_instance.clean_fields()
            model_instance.save()

            mail = EmailMessage(
                subject="New User Message",
                body=render_to_string('email/email.html', {
                    'subject': subject,
                    'fullname': fullname,
                    'email': email,
                    'phone_number': '***',
                    'message': message
                }),
                from_email='AjentX <email>',
                to=['support@ajentx.com', ],
                headers={'Reply-To': email}
            )

            mail.send()

            messages.success(request, "Message Sent")

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
