from django.shortcuts import render

# Create your views here.
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from booking.models import Room, Booking, Team
from booking.serializers import RoomSerializer, BookingSerializer, TeamSerializer

def home(request):
    return render(request, 'index.html')


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class TeamListCreateView(APIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        team = Team.objects.create(name=name)
        team.members.add(request.user)
        return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)


class BookRoomView(APIView):
    def post(self, request):
        room_id = request.data.get("room_id")
        slot = request.data.get("slot")
        team_id = request.data.get("team_id")

        if not room_id or not slot:
            return Response({"error": "room_id and slot required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slot_dt = datetime.fromisoformat(slot)
        except ValueError:
            return Response({"error": "Invalid datetime format"}, status=status.HTTP_400_BAD_REQUEST)

        room = get_object_or_404(Room, id=room_id)
        if Booking.objects.filter(room=room, slot=slot_dt).exists():
            return Response({"error": "Room already booked"}, status=status.HTTP_400_BAD_REQUEST)

        team = None
        if team_id:
            team = get_object_or_404(Team, id=team_id)
        booking = Booking.objects.create(room=room, slot=slot_dt, user=request.user if not team else None, team=team)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class CancelBookingView(APIView):
    def delete(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        if booking.user != request.user and not request.user.is_admin:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        booking.delete()
        return Response({"message": "Booking cancelled"}, status=status.HTTP_204_NO_CONTENT)


class AllBookedRoomsView(APIView):
    def get(self, request):
        if request.user.is_admin:
            bookings = Booking.objects.all()
        else:
            bookings = Booking.objects.filter(user=request.user) | Booking.objects.filter(team__members=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class AvailableRoomsView(APIView):
    def get(self, request):
        slot = request.query_params.get("slot")
        if not slot:
            return Response({"error": "slot query param required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            slot_dt = datetime.fromisoformat(slot)
        except ValueError:
            return Response({"error": "Invalid datetime"}, status=status.HTTP_400_BAD_REQUEST)

        booked = Booking.objects.filter(slot=slot_dt).values_list("room_id", flat=True)
        rooms = Room.objects.exclude(id__in=booked)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

