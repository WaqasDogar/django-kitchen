# templatetags/tag_library.py
from django import template
from django.db.models.fields import EmailField
register = template.Library()

from Myapp.models import *

@register.filter()
def to_int(value):
    return value.id

@register.filter()
def get_mail(value):
    obj=User.objects.all()
    for val in obj:
        if str(val)==str(value):
         return str(val.email)
