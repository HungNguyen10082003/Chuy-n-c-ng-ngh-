from django import admin
from .model import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')  # Thay đổi theo trường của model Item
    search_fields = ('name',)