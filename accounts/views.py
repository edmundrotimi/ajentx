from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.core.management import call_command
from contact.models import UserContact
from profiles.models import Profile
from django.contrib.auth.decorators import user_passes_test


User = get_user_model()

# test for only admin


def testuserrole(request):
    return User.objects.filter(is_superuser=True)


@user_passes_test(testuserrole)
def revisiondelete(request):
    if request.method == 'POST':
        app_name = request.POST.get('app_name')
        model_name = request.POST.get('model_name')
        path = request.POST.get('path')
        model_name = model_name.replace(" ", "")
        app_name_lower = app_name.lower()
        # call revision command
        call_command('deleterevisions',
                     f"{app_name_lower}.{model_name}", days=30)
        # sucess message
        messages.add_message(request, messages.SUCCESS,
                             'Revision(s) deleted successfully')
        # redirect to previous page
        return redirect(path)


class AccountSuspendedView(TemplateView):
    template_name = 'account/lockedout.html'


class AccountSuspension(LoginRequiredMixin, TemplateView):
    template_name = 'account/suspension.html'


def account_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'Your are now logged out')
    return redirect('home')


class AccountSignIn(View):

    def dispatch(self, request, *args, **kwargs):
        # check if user is logined in
        if self.request.user.is_authenticated:
            # get profile
            return HttpResponseRedirect(f'/account/create/profile/')
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
                return HttpResponseRedirect('/account/create/profile/')
        else:
            fullname = request.POST.get('fullname')
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST.get('message')

        try:

            model_instance = UserContact.objects.create(
                fullname=fullname,
                email=email,
                phone_number=phone_number,
                message=message
            )

            model_instance.clean_fields()
            model_instance.save()

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
                from_email=f'AjentX User Message <{email}>',
                to=['contact@ajentx.com>', ],
                headers={'Reply-To': email}
            )

            mail.send()

            messages.success(request, 'Message sent.')

            return HttpResponseRedirect('/accounts/login/')

        except ValidationError as e:
            string_error = ''
            for key, value in e:
                for i in value:
                    if 'Ensure this value has at least 10 characters' in i:
                        string_error = string_error + 'Message: '+i
                    else:
                        string_error = string_error + i
                messages.error(request, f'Error- \n {string_error}')

            return HttpResponseRedirect('/accounts/login/')


class AccountSignUp(SuccessMessageMixin, View):
    template_name = 'account/signup.html'
    success_message = 'Account created successfully'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        if request.POST.get('role') == 'user':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                user = User(username=username, first_name=first_name, last_name=last_name,
                            email=email, password=make_password(password1))
                try:
                    user.clean_fields()
                    user.save()

                    mail = EmailMessage(
                        subject="New Listing Message",
                        body=render_to_string('email/account-email.html'),
                        from_email='AjentX <noreply@ajentx.com>',
                        to=[email, ],
                    )

                    mail.send()

                    return HttpResponseRedirect('/accounts/login/')
                except ValidationError as e:
                    string_error = ''
                    for key, value in e:
                        for i in value:
                            string_error = string_error + i
                    messages.error(request, f'Error: {string_error}')
                    return HttpResponseRedirect('/accounts/signup/')
                except Exception as e:
                    messages.error(request, 'Error: Username already exist.')
                    return HttpResponseRedirect('/accounts/signup/')
            else:
                messages.error(request, 'Passwords do not match.')
                return HttpResponseRedirect('/accounts/signup/')
        else:
            fullname = request.POST.get('fullname')
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            message = request.POST.get('message')

            try:

                contact = UserContact(
                    fullname=fullname,
                    email=email,
                    phone_number=phone_number,
                    message=message
                )

                contact_check = contact.clean_fields()
                contact_check.save()

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
                    from_email=f'AjentX User Message <{email}>',
                    to=['contact@ajentx.com>', ],
                    headers={'Reply-To': email}
                )

                mail.send()

                messages.error(request, 'Message sent.')

                return HttpResponseRedirect('/accounts/signup/')

            except ValidationError as e:
                string_error = ''
                for key, value in e:
                    for i in value:
                        string_error = string_error + i
                messages.error(request, f'Error: {string_error}')

                return HttpResponseRedirect("/accounts/signup/")

    def dispatch(self, request, *args, **kwargs):
        # check if user is logined in
        if self.request.user.is_authenticated:
            # get profile
            return HttpResponseRedirect(f'/account/create/profile/')
        return super().dispatch(request, *args, **kwargs)
