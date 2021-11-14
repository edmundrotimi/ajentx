import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from autoslug import AutoSlugField
from multiselectfield import MultiSelectField
from validations import validateimage
from profiles.models import Profile

User = get_user_model()

status = {
    ('Sale', 'Sale'),
    ('Rent', 'Rent'),
    ('Lease', 'Lease'),
    ('Sold Out', 'Sold Out')
}

category = {
    ('Residential', 'Residential'),
    ('Commercial', 'Commercial'),
    ('Appartment', 'Appartment'),
    ('Industrial', 'Industrial'),
    ('Building', 'Building'),
    ('Land', 'Land'),
    ('Communal Land', 'Communal Land'),
    ('Offices', 'Offices'),
    ('Factory', 'Factory')
}

amenities = {
    ('Air Conditioning', 'Air Conditioning'),
    ('Cleaning Service', 'Cleaning Service'),
    ('Dishwasher', 'Dishwasher'),
    ('Hardwood Flows', 'Hardwood Flows'),
    ('Swimming Pool', 'Swimming Pool'),
    ('Outdoor Shower', 'Outdoor Shower'),
    ('Microwave', 'Microwave'),
    ('Pet Friendly', 'Pet Friendly'),
    ('Basketball Court', 'Basketball Court'),
    ('Refrigerator', 'Refrigerator'),
    ('Gym', 'Gym')
}


class PropertyListings(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='property_name',
                         unique_with=['id', 'date_created'])
    property_description = models.TextField(max_length=3000)
    rooms = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garage = models.IntegerField()
    garage_size = models.IntegerField(help_text='Sq Ft')
    year_built = models.DateField()
    property_status = models.CharField(
        choices=status, default='Sales', max_length=50)
    property_category = models.CharField(
        choices=category, default='Land', max_length=50)
    property_size = models.IntegerField(help_text='Sq Ft')
    property_price = models.IntegerField()
    amenities = MultiSelectField(
        choices=amenities, default='Swimming Pool', max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    nearby = models.TextField(max_length=1000)
    postal_code = models.IntegerField(verbose_name='Zip/Postal Code')
    neighborhood = models.CharField(max_length=100)
    feature_image_1 = models.ImageField(upload_to='property/featured/img',
                                        validators=[validateimage.clean_image])
    feature_image_2 = models.ImageField(upload_to='property/featured/img',
                                        validators=[validateimage.clean_image])
    feature_image_3 = models.ImageField(upload_to='property/featured/img',
                                        validators=[validateimage.clean_image])
    gallery_image_1 = models.ImageField(upload_to='property/gallery/photos',
                                        validators=[validateimage.clean_image])
    gallery_image_1_details = models.TextField(max_length=1000)
    gallery_image_2 = models.ImageField(upload_to='property/gallery/photos',
                                        validators=[validateimage.clean_image])
    gallery_image_2_details = models.TextField(max_length=1000)
    gallery_image_3 = models.ImageField(upload_to='property/gallery/photos',
                                        validators=[validateimage.clean_image])
    gallery_image_3_details = models.TextField(max_length=1000)
    publish = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
