from django.contrib import admin

# Register your models here.

from booking.models import User, Room, Team, Booking

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Team)
admin.site.register(Booking)
