from crispy_forms.utils import render_crispy_form
from jinja2 import Environment
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage
from .filters import datetimeformate, dateformate, timeformate, crispy, intcomma, unslugify
from django.contrib import messages


def JinjaEnvironment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'crispy': render_crispy_form,
        'get_messages': messages.get_messages,
        'trim_blocks' : True,
        'Istrip_blocks' : True,
    })
    env.filters.update({
        'datetimeformate':datetimeformate,
        'dateformate' : dateformate,
        'timeformate':timeformate,
        'crispy': crispy,
        'intcomma': intcomma,
        'unslugify':unslugify,
    })

    return env