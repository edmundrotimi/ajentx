# Add to your settings file
CONTENT_TYPES = ['video',]
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
#MAX_UPLOAD_SIZE = "10485760"

#Add to a form containing a FileField and change the field names accordingly.
from django.core.exceptions import ValidationError
from django.conf import settings

def clean_image(value):
    filesize = value.size
    if filesize > 209715.2:
        raise ValidationError('The maximum file size that can be uploaded is 200KB')
    else:
        return value