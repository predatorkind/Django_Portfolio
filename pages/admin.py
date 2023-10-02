from django.contrib import admin
from pages import models


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass
mods = models.get_models()
for mod in mods:
    try:
        admin.site.register(mod)
    except:
        continue