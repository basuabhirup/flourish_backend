from django.shortcuts import render

events = [
    {
        "title": "#WP21 - WordPress 21st Anniversary Meetup & Celebration",
        "description": "",
        "date": "Sat, Jun 1 2024",
        "time": "6:00 PM IST",
        "location": "Mayur Vihar, Delhi",
        "category": "Tech",
        "organizer": "Ajitesh Sharma",
        "capacity": "",
        "image": "https://secure.meetupstatic.com/photos/event/1/8/0/8/600_521346152.webp?w=384"
    },
    {
        "title": "Ladakh Calling - An immersive experience Landscapes, Culture & Heritage",
        "description": "",
        "date": "Fri, Jun 14 2024",
        "time": "1:00 PM IST",
        "location": "East of Kailash, Delhi",
        "category": "Hiking",
        "organizer": "Rajesh Trivedi",
        "capacity": "",
        "image": "https://secure.meetupstatic.com/photos/event/6/1/c/event_521041564.webp?w=384"
    },
    {
        "title": "Elixir Delhi + FPIndia Combined June Meetup",
        "description": "",
        "date": "Sun, Jun 2 2024",
        "time": "1:00 PM IST",
        "location": "29, Rajpur Road · Delhi",
        "category": "Tech",
        "organizer": "Delhi Elixir Meetup Group",
        "capacity": "",
        "image": "https://secure.meetupstatic.com/photos/event/1/3/e/e/600_521345102.webp?w=384"
    },
    {
        "title": "#WP21 - WordPress 21st Anniversary Meetup & Celebration",
        "description": "",
        "date": "Sat, Jun 1 2024",
        "time": "6:00 PM IST",
        "location": "Mayur Vihar, Delhi",
        "category": "Tech",
        "organizer": "Ajitesh Sharma",
        "capacity": "",
        "image": "https://secure.meetupstatic.com/photos/event/1/8/0/8/600_521346152.webp?w=384"
    },
    {
        "title": "#WP21 - WordPress 21st Anniversary Meetup & Celebration",
        "description": "",
        "date": "Sat, Jun 1 2024",
        "time": "6:00 PM IST",
        "location": "Mayur Vihar, Delhi",
        "category": "Tech",
        "organizer": "Ajitesh Sharma",
        "capacity": "",
        "image": "https://secure.meetupstatic.com/photos/event/1/8/0/8/600_521346152.webp?w=384"
    },
]

# Create your views here.
def index(request):
    return render(request, "events/index.html", {
        "events": events
    })