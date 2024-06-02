from django.shortcuts import render

events = [
   {
    "id": 1,
    "title": "WordPress 21st Anniversary Meetup & Celebration",
    "description": "Join us for a celebration of the 21st anniversary of WordPress! This meetup will be a great opportunity to connect with other WordPress enthusiasts in Delhi, share your experiences, and learn about the latest developments in the WordPress world. We'll have talks, demos, and plenty of time for networking. Whether you're a seasoned developer or just getting started with WordPress, this meetup is for you!",
    "date": "Sat, Jun 1 2024",
    "time": "6:00 PM IST",
    "location": "Mayur Vihar, Delhi",
    "category": "Tech",
    "organizer": "Ajitesh Sharma",
    "capacity": "",
    "image": "https://secure.meetupstatic.com/photos/event/1/8/0/8/600_521346152.webp?w=384"
  },
  {
    "id": 2,
    "title": "Ladakh Calling - Landscapes, Culture & Heritage",
    "description": "Calling all adventure seekers! Join us for a unique opportunity to explore the breathtaking landscapes, rich culture, and ancient heritage of Ladakh. This trip will take you to some of the most stunning locations in the Himalayas, including Pangong Tso lake, Nubra Valley, and the Leh Palace. You'll also have the chance to experience the traditional Ladakhi way of life and learn about the region's fascinating history. This is a trip you won't forget!",
    "date": "Fri, Jun 14 2024",
    "time": "1:00 PM IST",
    "location": "East of Kailash, Delhi",
    "category": "Hiking",
    "organizer": "Rajesh Trivedi",
    "capacity": "",
    "image": "https://secure.meetupstatic.com/photos/event/6/1/c/event_521041564.webp?w=384"
  },
  {
    "id": 3,
    "description": "Calling all Elixir and functional programming enthusiasts in Delhi! Join us for a combined meetup of the Delhi Elixir Group and FPIndia. This meetup will be a great opportunity to learn about the latest developments in the Elixir and functional programming worlds, share your experiences, and network with other developers. We'll have talks, demos, and plenty of time for socializing. Whether you're a seasoned Elixir developer or just curious about functional programming, this meetup is for you!",
    "title": "Elixir Delhi + FPIndia Combined June Meetup",
    "date": "Sun, Jun 2 2024",
    "time": "1:00 PM IST",
    "location": "29, Rajpur Road · Delhi",
    "category": "Tech",
    "organizer": "Delhi Elixir Group",
    "capacity": "",
    "image": "https://secure.meetupstatic.com/photos/event/1/3/e/e/600_521345102.webp?w=384"
  },
  {
    "id": 4,
    "title": "Community Clay Workshop: Handbuild a Mug",
    "description": " Unleash your inner artist and learn the basics of handbuilding with clay! In this workshop, you'll be guided by experienced potter [Instructor Name] as you create your very own mug. This is a great opportunity to relax, have fun, and get creative. All skill levels are welcome, and no prior experience is necessary. Materials and refreshments will be provided.",
    "date": "Wed, Jun 5 2024",
    "time": "7:00 PM IST",
    "location": "Khan Market, Delhi",
    "category": "Arts & Crafts",
    "organizer": "The Clay Studio",
    "capacity": "10",
    "image": "https://plus.unsplash.com/premium_photo-1661331633771-cb5ad3b7a7e9?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    "id": 5,
    "title": "Introduction to Data Science with Python",
    "description": "Are you curious about data science but don't know where to start? This workshop is a perfect introduction for beginners! You'll learn the fundamentals of data science, including data manipulation, analysis, and visualization using Python. No prior programming experience is required. By the end of the workshop, you'll be able to work with real-world datasets and gain the confidence to explore data science further.",
    "date": "Thu, Jun 6 2024",
    "time": "6:00 PM IST",
    "location": "Co-working space, Gurgaon",
    "category": "Tech",
    "organizer": "Data Enthusiasts Delhi",
    "capacity": "15",
    "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    "id": 6,
    "title": "Book Discussion: Sapiens: A Brief History of Humankind",
    "description": "Join us for a lively discussion about Yuval Noah Harari's groundbreaking book, Sapiens: A Brief History of Humankind. This book explores the history of our species, from our origins as hunter-gatherers to the present day. We'll delve into topics like the development of language, agriculture, and civilization. This is a great opportunity to meet other book lovers and share your thoughts on this thought-provoking book.",
    "date": "Tue, Jun 4 2024",
    "time": "7:30 PM IST",
    "location": "Cafe Mocha, Connaught Place",
    "category": "Book Club",
    "organizer": "Delhi Bookworms",
    "capacity": "20",
    "image": "https://images.unsplash.com/photo-1605732021795-68ea025c3d37?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    "id": 7,
    "title": "Delhi Street Food Tour: A Culinary Adventure",
    "description": "Embark on a delicious adventure through the vibrant streets of Delhi! This food tour will take you to some of the best hidden gems of Delhi's street food scene. You'll sample a variety of traditional dishes, from savory samosas and spicy curries to sweet jalebis and refreshing lassi. Along the way, you'll learn about the history and culture of Delhi's street food. This is a must-do for any foodie visiting Delhi!",
    "date": "Sat, Jun 8 2024",
    "time": "11:00 AM IST",
    "location": "Chandni Chowk Market",
    "category": "Food & Drink",
    "organizer": "Delhi Food Trails",
    "capacity": "12",
    "image": "https://images.unsplash.com/photo-1616486447077-f8d3f7bae6b7?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    "id": 8,
    "title": "Bollywood Dance Workshop: Learn the Basics",
    "description": "Get ready to move and groove! This Bollywood dance workshop will teach you the basic steps and techniques of Bollywood dancing. You'll learn how to perform energetic routines to popular Bollywood songs. This is a fun and energetic way to get some exercise and learn about Indian culture. No prior dance experience is necessary. Wear comfortable clothing and shoes that you can move in easily.",
    "date": "Fri, Jun 7 2024",
    "time": "5:00 PM IST",
    "location": "Saket Community Center",
    "category": "Fitness & Dance",
    "organizer": "Masti Ki Pathshala",
    "image": "https://plus.unsplash.com/premium_vector-1682305697455-23e54add66b2?bg=FFFFFF&q=80&w=1800&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    "id": 9,
    "title": "Yoga for Beginners: Find Your Inner Peace",
    "description": "Are you looking for a way to de-stress and improve your overall well-being? This yoga class for beginners is a perfect introduction to the practice of yoga. You'll learn basic postures (asanas), breathing techniques (pranayama), and relaxation techniques. This class is suitable for all levels of fitness and experience. Bring a yoga mat or a comfortable towel.",
    "date": "Mon, Jun 10 2024",
    "time": "9:00 AM IST",
    "location": "Hauz Khas Park",
    "category": "Fitness & Wellness",
    "organizer": "Yogshala Delhi",
    "capacity": "15",
    "image": "https://images.unsplash.com/photo-1616699002805-0741e1e4a9c5?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    "id": 10,
    "title": "Creative Writing Workshop: Spark Your Imagination",
    "description": "Do you have a story waiting to be told? This creative writing workshop will help you tap into your creativity and develop your writing skills. You'll participate in writing exercises, receive feedback on your work, and learn from experienced writers. This workshop is perfect for aspiring writers of all levels. Bring your pen and notebook (or laptop) and get ready to write!",
    "date": "Wed, Jun 12 2024",
    "time": "6:30 PM IST",
    "location": "Co-working space, Noida",
    "category": "Arts & Creativity",
    "organizer": "Write Tribe Delhi",
    "capacity": "8",
    "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    "id": 11,
    "title": "Sustainable Living Workshop: Reduce Your Impact",
    "description": "Are you concerned about the environment and want to make a difference? This sustainable living workshop will teach you practical tips on how to reduce your environmental impact in everyday life. You'll learn about topics like composting, reducing waste, and conserving energy. This workshop is a great way to live a more sustainable lifestyle and protect our planet.",
    "date": "Sat, Jun 15 2024",
    "time": "2:00 PM IST",
    "location": "Community Center, Dwarka",
    "category": "Sustainability",
    "organizer": "Eco Warriors Delhi",
    "capacity": "25",
    "image": "https://images.unsplash.com/photo-1483752317269-423e6ad6fe2a?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    "id": 12,
    "title": "Film Screening & Discussion: The Lunchbox",
    "description": "Join us for a screening of the heartwarming Indian film, The Lunchbox, followed by a discussion. This movie tells the story of an unlikely friendship that develops between a lonely widower and a young housewife through a mistaken lunch delivery. This is a great opportunity to enjoy a beautiful film and engage in a meaningful conversation.",
    "date": "Thu, Jun 13 2024",
    "time": "6:00 PM IST",
    "location": "Alliance Française de Delhi",
    "category": "Film & Entertainment",
    "organizer": "Delhi Cine Club",
    "capacity": "30",
    "image": "https://plus.unsplash.com/premium_vector-1689096868982-2c5e8a4bd0b4?bg=FFFFFF&q=80&w=1800&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  }
]

# Create your views here
def index(request):
    return render(request, "events/index.html", {
        "events": events[-8:]
    })
    

def event_detail(request, event_id):
    event = events[event_id -1]
    return render(request, "events/event_detail.html", {
        "event": event
    })