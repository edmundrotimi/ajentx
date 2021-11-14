from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import generic

from blog.models import BlogComment
from .models import UserContact


class Contact(generic.View):
    template_name = 'pages/contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone_number = request.POST['phone']
        subject = request.POST['subject']
        message = request.POST['message']

        try:

            model_instance = UserContact(
                fullname=fullname,
                email=email,
                phone_number=phone_number,
                subject=subject,
                message=message
            )

            model_instance.clean_fields()
            model_instance.save()

            mail = EmailMessage(
                subject="New User Message",
                body=render_to_string('email/email.html', {
                    'subject': 'New User Message',
                    'fullname': fullname,
                    'email': email,
                    'phone_number': phone_number,
                    'message': f'{subject} \n {message}'
                }),
                from_email='AjentX <email>',
                to=['contact@ajentx.com', ],
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
