## Django Packages
from django.contrib import admin
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls import path
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string

## Custom Libs ##
from lib.functions import send_mail_with_html

## App packages
from .models import *
from tags_input import admin as tags_input_admin

############################################################################


class TourAdmin(tags_input_admin.TagsInputAdmin):
    list_display = (
        'name',
        'description',
    )

admin.site.register(Tour, TourAdmin)
