from django.contrib import admin
from .models import Event, Guest, GuestCategory, RelatedTo

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_date', 'ceremony_location', 'reception_location', 'groom_name', 'bride_name')
    search_fields = ('groom_name', 'bride_name')
    list_filter = ('event_date', 'ceremony_location')

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'additional_guests_amount', 'category', 'event')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('category', 'event')

@admin.register(GuestCategory)
class GuestCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('category_name',)

@admin.register(RelatedTo)
class RelatedToAdmin(admin.ModelAdmin):
    list_display = ('id', 'related_name',)
    search_fields = ('related_name',)