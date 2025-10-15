Workspace Booking System

A Django REST Framework (DRF) project to manage workspace room bookings, cancellations, availability, and teams. Supports Private Rooms, Conference Rooms, and Shared Desks with booking priorities, slots, and role-based access.

Table of Contents :
	Project Features
	System Requirements
	Installation
	Database Setup & Migrations
	Running the Server
	API Authentication
	API Endpoints
	Testing with Postman
	Admin Interface
	Project Features

Room Types:
	8 Private Rooms (1 user)
	4 Conference Rooms (3+ members)
	3 Shared Desks (up to 4 users each)

Booking Rules:
	Users can book only one slot at a time.
	Overlapping slots are blocked for the same room.
	Children (age <10) counted in headcount but do not occupy seats.
	Teams: Groups of users can book conference rooms.
	Role-based access: Admin vs normal users.
	Available Rooms Query: Check rooms by slot.
	Cancel Booking: Users/admins can cancel bookings.
	Pagination: On large lists of bookings.

System Requirements :-

	Python 3.12+
	Django 4.x+
	Django REST Framework
	PostgreSQL/MySQL/SQLite (SQLite default)

Installation :-

	Clone the repository:
		git clone https://github.com/satyapateldp/workspace_booking.git
		cd workspace_booking


	Create a virtual environment:
		python -m venv venv
		source venv/bin/activate   # Linux/macOS
		venv\Scripts\activate      # Windows

	Install dependencies:	
		pip install -r requirements.txt

Database Setup & Migrations :-
	Apply migrations:	
	python manage.py makemigrations
	python manage.py migrate


	Seed default rooms:
	The app automatically creates 15 rooms (Private, Conference, Shared Desks) on migration.
	
	Create superuser (optional):	
		python manage.py createsuperuser
	
	Running the Server
	python manage.py runserver

Server runs at:
	http://127.0.0.1:8000/

API base path:
	http://127.0.0.1:8000/api/v1/

API Authentication :-

	Uses JWT Authentication.
	
	Endpoints for authentication:
	
	Endpoint	Method	Description
	/api/v1/auth/register/	POST	Register new user
	/api/v1/auth/login/	POST	Login and get JWT tokens
	/api/v1/auth/token/refresh/	POST	Refresh JWT token

Headers for protected endpoints:
	Authorization: Bearer <access_token>

API Endpoints
Endpoint	Method	Description
	/api/v1/teams/	GET / POST	List/Create teams
	/api/v1/bookings/	POST	Book a room (user or team)
	/api/v1/bookings/<id>/cancel/	DELETE	Cancel booking
	/api/v1/bookings/booked/	GET	List booked rooms
	/api/v1/rooms/available/?slot=YYYY-MM-DDTHH:MM:SS	GET	Get available rooms for a slot
Booking Example

POST /api/v1/bookings/

{
  "room_id": 1,
  "slot": "2025-10-13T09:00:00"
}


Response:

{
  "id": 1,
  "room": {"id":1,"name":"Private Room 1","room_type":"PRIVATE","capacity":1},
  "user": {"id":1,"username":"alice","age":28,"is_admin":false},
  "team": null,
  "slot": "2025-10-13T09:00:00"
}

Testing with Postman

Import collection (optional).

Set Authorization header with Bearer <access_token>.

Test endpoints:

		Register/Login user
		
		Create/List teams
		
		Book a room
		
		Cancel a booking
		
		List booked rooms
		
		Check available rooms

Admin Interface

	Available at:
	
	http://127.0.0.1:8000/admin/
	
	
	Login using superuser credentials.
	
	Manage Users, Rooms, Bookings, Teams directly.
