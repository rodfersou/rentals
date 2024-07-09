from django.apps import apps
from django.contrib import admin
from django.contrib.admin import sites

for model in apps.get_models():
    try:
        admin.site.register(model)
    except sites.AlreadyRegistered:
        ...
