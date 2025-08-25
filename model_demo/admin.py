from django.contrib import admin
from .models import Group, Item, Feedback, Purchase

admin.site.register(Group)
admin.site.register(Item)
admin.site.register(Feedback)
admin.site.register(Purchase)
