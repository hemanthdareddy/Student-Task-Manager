from django.contrib import admin
from .models import Task, Subject, Badge, Profile # Add Badge and Profile

admin.site.register(Task)
admin.site.register(Subject)
admin.site.register(Badge)   # Add this
admin.site.register(Profile) # Add this