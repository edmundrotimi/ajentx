from jinja2 import Markup
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form

def dateformate(value):
    return f'{value.strftime("%d")} {value.strftime("%d")}\' {value.strftime("%-y")}'

def timeformate(value):
    return f'{value.strftime("%H")}:{value.strftime("%M")} {value.strftime("%p")}'

def datetimeformate(value):
    return f'{value.strftime("%d")} {value.strftime("%d")}\' {value.strftime("%-y")} {value.strftime("%H")}:{value.strftime("%M")} {value.strftime("%p")}'
    

def crispy(form):
    return as_crispy_form(form, 'Bootstrap4', label_class="", field_class="")


def intcomma(value):
    value_int = int(value)
    return f'{value_int:,}'