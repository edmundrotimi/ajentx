from django import forms
from django.forms import models
from .models import status, category, amenities, PropertyListings
from validations import validateimage
from profiles.models import TourSchedule, AgentContact


class ListingsForms(forms.ModelForm):
    property_name = forms.CharField(max_length=200)
    property_description = forms.CharField(
        max_length=1000, widget=forms.Textarea())
    rooms = forms.IntegerField()
    bedrooms = forms.IntegerField()
    bathrooms = forms.IntegerField()
    garage = forms.IntegerField()
    garage_size = forms.IntegerField(help_text='Sq Ft', )
    year_built = forms.DateField(widget=forms.DateInput(attrs={
        'id': 'datepicker'}))
    property_status = forms.ChoiceField(choices=status)
    property_category = forms.ChoiceField(choices=category)
    property_size = forms.IntegerField(help_text='Sq Ft')
    property_price = forms.IntegerField()
    amenities = forms.MultipleChoiceField(
        choices=amenities)
    address = forms.CharField(max_length=200)
    country = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    nearby = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
                             'placeholder': 'eg. Institute of Technology (1.42 km), Finest Rstaurant (1.42 km)'}))
    postal_code = forms.IntegerField(label='Zip/Postal Code')
    neighborhood = forms.CharField(max_length=100)
    feature_image_1 = forms.ImageField(required=False, validators=[
                                       validateimage.clean_image], widget=forms.FileInput(attrs={'class': 'theme-btn btn-one'}))
    feature_image_2 = forms.ImageField(required=False, validators=[
                                       validateimage.clean_image], widget=forms.FileInput(attrs={'class': 'theme-btn btn-one'}))
    feature_image_3 = forms.ImageField(required=False, validators=[
                                       validateimage.clean_image], widget=forms.FileInput(attrs={'class': 'theme-btn btn-one'}))
    gallery_image_1 = forms.ImageField(required=False, validators=[
                                       validateimage.clean_image], widget=forms.FileInput(attrs={'class': 'theme-btn btn-one'}))
    gallery_image_1_details = forms.CharField(
        max_length=1000, widget=forms.Textarea())
    gallery_image_2 = forms.ImageField(required=False, validators=[
                                       validateimage.clean_image], widget=forms.FileInput(attrs={'class': 'theme-btn btn-one'}))
    gallery_image_2_details = forms.CharField(
        max_length=1000, widget=forms.Textarea())
    gallery_image_3 = forms.ImageField(required=False, validators=[
                                       validateimage.clean_image], widget=forms.FileInput(attrs={'class': 'theme-btn btn-one'}))
    gallery_image_3_details = forms.CharField(
        max_length=1000, widget=forms.Textarea())

    class Meta:
        model = PropertyListings
        exclude = ('id', 'user', 'publish', 'date_created', 'last_updated')


class TourForm(forms.ModelForm):
    class Meta:
        model = TourSchedule
        fields = ('full_name', 'email', 'phone_number',
                  'tour_date', 'tour_time', 'message')


class AgentContactForm(forms.ModelForm):
    class Meta:
        model = AgentContact
        fields = ('contact_full_name', 'contact_email', 'contact_phone_number',
                  'contact_message')
