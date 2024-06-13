from django.shortcuts import render
from .models import Event, User, Group, Registration, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q


# Create your views here
def index(request):
    events = Event.objects.order_by('-date', '-time')[:4]
    groups = Group.objects.filter(privacy_setting='public').order_by('-created_at')[:4]
    return render(request, "events/index.html", {
        "events": events,
        "groups": groups
    })
    

def event_detail(request, event_id):
  try:
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_detail.html', {
      'event': event
      })
  except Event.DoesNotExist:
    return render(request, 'events/404.html')
  
  
def group_detail(request, group_id):
  try:
    group = Group.objects.get(pk=group_id)
    
    if group.privacy_setting == 'public' or (request.user.is_authenticated and group.members.filter(pk=request.user.pk).exists()):
      events = group.events.all()
      members = group.members.all()
      owner = group.owner
      
      return render(request, 'events/group_detail.html', {
        'group': group,
        'upcoming_events': events,
        'past_events': events,
        'members': members,
        'owner': owner
      })
    else:
      return render(request, 'events/404.html')
  except Group.DoesNotExist:
    return render(request, 'events/404.html')

    
def all_events(request):
    events = Event.objects.all()
    groups = Group.objects.filter(privacy_setting='public').order_by('-created_at')
    return render(request, "events/events.html", {
        "events": events,
        "groups": groups
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Succesfully logged in.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username and/or password.'}, status=500)
    else:
        return render(request, 'events/404.html')


@csrf_exempt
def logout_view(request):
  if request.method == "POST":
    logout(request)
    return JsonResponse({'message': 'Succesfully logged out.'}, status=200)
  else:
      return render(request, 'events/404.html')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return JsonResponse({'error': 'Passwords must match!'}, status=400)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return JsonResponse({'error': 'Username already taken!'}, status=500)
        
        login(request, user)
        return JsonResponse({'message': 'Succesfully signed up.'}, status=200)
    else:
        return render(request, 'events/404.html')
    
  
@login_required
def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'events/404.html')

    user = request.user

    return render(request, 'events/profile.html', {
        'user': user
        })
    

@login_required 
def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'events/404.html')

    user = request.user

    # Attended events
    attended_upcoming_events_reg = Registration.objects.filter(Q(user=user), Q(event__date__gte=timezone.now().date())).defer('user').select_related('event')
    attended_past_events_reg = Registration.objects.filter(Q(user=user), Q(event__date__lt=timezone.now().date())).defer('user').select_related('event')
    
    upcoming_event_ids = [reg.event.id for reg in attended_upcoming_events_reg]
    past_event_ids = [reg.event.id for reg in attended_past_events_reg]
    
    attended_upcoming_events = Event.objects.filter(pk__in=upcoming_event_ids)
    attended_past_events = Event.objects.filter(pk__in=past_event_ids)

    # Hosted events
    hosted_upcoming_events = Event.objects.filter(host=user, date__gte=timezone.now().date())
    hosted_past_events = Event.objects.filter(host=user, date__lt=timezone.now().date())
    
    groups = Group.objects.filter(members__in=[user])
    print(groups)

    return render(request, 'events/dashboard.html', {
        'user': user,
        'attended_upcoming_events': attended_upcoming_events,
        'attended_past_events': attended_past_events,
        'hosted_upcoming_events': hosted_upcoming_events,
        'hosted_past_events': hosted_past_events,
        'groups': groups
    })

    
@login_required
def create_group(request):
  if request.method == "POST" and request.user.is_authenticated:
    user = request.user
    group_name = request.POST.get('name')
    group_description = request.POST.get('description')
    privacy_setting = request.POST.get('privacy_setting', 'public')  # Default to public
    group_image_url = request.POST.get('image_url')
    
    if not group_name:
      return JsonResponse({'error': 'Please enter a group name.'}, status=400)
    
    try:
      group = Group.objects.create(
          name=group_name,
          description=group_description,
          owner=user,
          privacy_setting=privacy_setting,
          image_url=group_image_url
      )
      # Add the owner as a member of the group
      group.members.add(user)
    except IntegrityError:
      # Handle potential duplicate group names (optional)
      return JsonResponse({'error': 'Group creation failed.'}, status=500)
    
    # Success response     
    return JsonResponse({'message': 'Group created successfully!', 'group': {
      'id': group.id,
      'name': group.name,
      'description': group.description,
      'privacy_setting': group.privacy_setting
    }}, status=201)
  else:
    return JsonResponse({'error': 'Invalid request!'}, status=400)
  
  
@login_required
def create_event(request):
  if request.method == "POST" and request.user.is_authenticated:
    user = request.user
    event_title = request.POST.get('title')
    event_description = request.POST.get('description')
    event_date = request.POST.get('date')
    event_time = request.POST.get('time')
    event_location = request.POST.get('location')
    event_category = request.POST.get('category')  # Assuming category is a foreign key ID

    # Optional fields
    event_capacity = request.POST.get('capacity')
    event_image = request.POST.get('image')

    if not event_title:
      return JsonResponse({'error': 'Please enter event title.'}, status=400)

    # Additional validation
    try:
      from datetime import datetime  # Import for date parsing
      datetime.strptime(event_date, '%Y-%m-%d')  # Check for YYYY-MM-DD format
    except ValueError:
      return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    try:
      datetime.strptime(event_time, '%H:%M')  # Check for HH:MM format
    except ValueError:
      return JsonResponse({'error': 'Invalid time format. Use HH:MM'}, status=400)

    try:
      event = Event.objects.create(
          title=event_title,
          description=event_description,
          date=event_date,
          time=event_time,
          location=event_location,
          category_id=event_category,  # Assuming category is a foreign key ID
          host=user,  
          capacity=event_capacity,
          image=event_image,     
      )
    except IntegrityError as e:
      # Handle specific exceptions (optional)
      if "duplicate values" in str(e):  # Check for duplicate event names
        return JsonResponse({'error': 'Event with this name already exists.'}, status=400)
      else:
        return JsonResponse({'error': 'Event creation failed.'}, status=500)

    # Success response with limited event data
    return JsonResponse({'message': 'Event created successfully!', 'event': {
      'id': event.id,
      'name': event.title
    }}, status=201)
  else:
    return JsonResponse({'error': 'Invalid request!'}, status=400)


@login_required
def categories(request):
  if request.method == "GET":
    categories = Category.objects.all().order_by('name')
    category_data = []
    for category in categories:
      category_data.append({
        'id': category.id,
        'name': category.name,
      })
    return JsonResponse({'categories': category_data}, status=200)
  else:
    return JsonResponse({'error': 'Invalid request method. Use GET.'}, status=400)