from django import forms
from django.db.models import fields
from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'state', 'country', 'city', 'phone_number',
                  'company_name', 'picture', 'bio', 'status', 'social_facebook',
                  'social_twitter', 'social_linkedin')
