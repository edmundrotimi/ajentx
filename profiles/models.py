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
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    slug = AutoSlugField(populate_from='first_name',
                         unique_with=['id', 'date_created'])
    country = models.CharField(max_length=50, default='', null=True, )
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=50, default='---', blank=True, null=True)
    picture = models.ImageField(upload_to='user/profile/photos',
                                blank=True, null=True, validators=[validateimage.clean_image])
    bio = models.TextField(max_length=2500, validators=[
                           MinLengthValidator(500)])
    status = models.CharField(
        max_length=50, choices=profile_status, default='Active')
    publish = models.BooleanField(
        default=True, help_text='useful for profile account suspention')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_login}'
