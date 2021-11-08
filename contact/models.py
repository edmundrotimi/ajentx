from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField
from django.core.validators import MinLengthValidator


class Contact(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(max_length=2500, validators=[MinLengthValidator(30)])
    date_created = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Contact Messages'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-date_created']
