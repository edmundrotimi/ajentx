import uuid
from datetime import datetime, time
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from autoslug import AutoSlugField
from django.core.validators import MinLengthValidator
from validations import validateimage

User = get_user_model()

profile_status = (
    ('Seller', 'Seller'),
    ('Brooker/Realtor', 'Brooker/Realtor'),
    ('Buyer', 'Buyer'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='first_name',
                         unique_with=['id', 'date_created'])
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    company_name = models.CharField(
        max_length=50, default='---', blank=True, null=True)
    picture = models.ImageField(upload_to='user/profile/photos',
                                validators=[validateimage.clean_image])
    bio = models.TextField(max_length=2500, validators=[
                           MinLengthValidator(300)])
    status = models.CharField(
        max_length=50, choices=profile_status, default='Seller')
    social_facebook = models.URLField(default='https://www.bbc.com')
    social_twitter = models.URLField(default='https://www.bbc.com')
    social_linkedin = models.URLField(default='https://www.bbc.com')
    publish = models.BooleanField(
        default=True, help_text='useful for profile account suspention')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_login}'


class AgentContact(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_full_name = models.CharField(
        max_length=50, verbose_name='Full Name')
    slug = AutoSlugField(populate_from='contact_full_name',
                         unique_with=['id', 'date_created'])
    contact_email = models.EmailField(verbose_name='Email')
    contact_phone_number = models.CharField(
        max_length=50, verbose_name='Phone Number')
    contact_message = models.TextField(max_length=2500, verbose_name='Message')
    publish = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return f'Message By: {self.user.first_name}'


class TourSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='full_name',
                         unique_with=['id', 'date_created'])
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    message = models.TextField(max_length=2500)
    tour_date = models.DateField()
    tour_time = models.TimeField()
    publish = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return f'Message By: {self.user.first_name}'
