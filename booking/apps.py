from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import connection


class BookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "booking"

    def ready(self):

        def create_default_rooms(sender, **kwargs):
            # Lazy import to avoid AppRegistryNotReady
            from .models import Room

            # Ensure database tables exist
            if not connection.introspection.table_names():
                return  # Skip if tables not yet created

            if Room.objects.exists():
                return  # Already seeded

            # Seed Private Rooms
            for i in range(1, 9):
                Room.objects.create(
                    name=f"Private Room {i}",
                    room_type="PRIVATE",
                    capacity=1
                )

            # Seed Conference Rooms
            for i in range(1, 5):
                Room.objects.create(
                    name=f"Conference Room {i}",
                    room_type="CONFERENCE",
                    capacity=10
                )

            # Seed Shared Desks
            for i in range(1, 4):
                Room.objects.create(
                    name=f"Shared Desk {i}",
                    room_type="SHARED",
                    capacity=4
                )

            # Uncomment for debug
            # print("✅ Default 15 rooms created successfully.")

        post_migrate.connect(create_default_rooms, sender=self)
