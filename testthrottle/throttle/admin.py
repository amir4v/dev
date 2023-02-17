from django.contrib import admin
from .models import Memory, Limit, Condition
# Register your models here.
admin.site.register(Memory)
admin.site.register(Limit)
admin.site.register(Condition)
