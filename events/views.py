from django.shortcuts import render
from .models import Event, User, Group, Registration
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q


# Create your views here
def index(request):
    events = Event.objects.order_by('-date', '-time')[:8]
    return render(request, "events/index.html", {
        "events": events
    })
    

def event_detail(request, event_id):
  try:
    event = Event.objects.get(pk=event_id) 
    context = {'event': event}
    return render(request, 'events/event_detail.html', context)
  except Event.DoesNotExist:
    return render(request, 'events/404.html')

    
def all_events(request):
    events = Event.objects.all()
    return render(request, "events/events.html", {
        "events": events
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
    
    
def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'events/404.html')

    user = request.user

    return render(request, 'events/profile.html', {
        'user': user
        })
    
    
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
    
    print(attended_upcoming_events)
    print(attended_past_events)

    return render(request, 'events/dashboard.html', {
        'user': user,
        'attended_upcoming_events': attended_upcoming_events,
        'attended_past_events': attended_past_events,
        'hosted_upcoming_events': hosted_upcoming_events,
        'hosted_past_events': hosted_past_events,
    })

    
    
@csrf_exempt
def create_group(request):
  if request.method == "POST" and request.user.is_authenticated:
    user = request.user
    group_name = request.POST.get('name')
    group_description = request.POST.get('description')
    privacy_setting = request.POST.get('privacy_setting', 'public')  # Default to public
    
    if not group_name:
      return JsonResponse({'error': 'Please enter a group name.'}, status=400)
    
    try:
      group = Group.objects.create(
          name=group_name,
          description=group_description,
          owner=user,
          privacy_setting=privacy_setting
      )
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