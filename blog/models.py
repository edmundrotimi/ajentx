from autoslug.fields import AutoSlugField
from django.db import models
from django.utils import timezone
from django.views.generic import detail
from django.contrib.auth import get_user_model
from profiles.models import Profile
from validations import validateimage
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()

categories = (
    ('Home improvement', 'Home improvement'),
    ('Architecture', 'Architecture'),
    ('Tips and advice', 'Tips and advice'),
    ('Interior', 'Interior'),
    ('Real Estate', 'Real Estate')
)


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='title',
                         unique_with=['id', 'date_created'], default='')
    feature_image = models.ImageField(upload_to='post/featured/img',
                                      validators=[validateimage.clean_image])
    detail = RichTextUploadingField(max_length=5000, help_text='post details')
    category = models.CharField(
        choices=categories, default='Architecture', max_length=50)
    tags = models.CharField(max_length=100, help_text='sperate with ","')
    author_image = models.ImageField(upload_to='post/author/img',
                                     validators=[validateimage.clean_image], null=True)
    publish = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-last_updated',)


class BlogComment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000, help_text='post details')
    publish = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ('-last_updated',)
