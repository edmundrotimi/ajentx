from django.core.mail import EmailMessage
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from validate_email import validate_email
from contact.models import Contact


def user_request(request):
    fullname = request.POST.get('fullname')
    email = request.POST['email']
    phone_number = request.POST['phone_number']
    message = request.POST.get('message')

    is_valid_email = validate_email(
        email_address=email.strip(),
        check_format=True,
        check_blacklist=True,
        check_dns=True,
        dns_timeout=10,
        check_smtp=True,
        smtp_timeout=10,
        smtp_helo_host=None,
        smtp_from_address=None,
        smtp_skip_tls=False,
        smtp_tls_context=None,
        smtp_debug=False
    )

    if is_valid_email == True or is_valid_email == None:
        Contact.objects.create(
            fullname=fullname,
            email=email,
            phone_number=phone_number,
            message=message
        )

        # send email
        mail = EmailMessage(
            subject='User Enquiry',
            body=render_to_string(template_name='email/email.html', context={
                'subject': 'User Enquiry',
                'fullname': fullname,
                'email': email,
                'phone_number': phone_number,
                'message': message,
            }),
            from_email=email,
            to=['AjentX User Request <contact@ajentx.com>',],
            headers={'Reply-To': email}
        )

        mail.send()

        messages.error(request, 'Message sent successfully.')

        return HttpResponseRedirect('/')
    else:
        messages.error(request, 'Invalid form field')
