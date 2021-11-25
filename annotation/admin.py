from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Name)
admin.site.register(Category)
admin.site.register(Leader)
admin.site.register(Annotator)
admin.site.register(Batch)
