from django.shortcuts import render
from .models import Event, User, Group, Registration, Category, UserProfile
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
import json
from django.core.exceptions import ObjectDoesNotExist




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
      upcoming_events = group.events.filter(date__gte=timezone.now().date())
      past_events = group.events.filter(date__lt=timezone.now().date())
      members = group.members.all()
      owner = group.owner
      
      return render(request, 'events/group_detail.html', {
        'group': group,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        
        if not username:
          return JsonResponse({'error': 'Must provide username!'}, status=400)
        
        if not email:          
          return JsonResponse({'error': 'Must provide email!'}, status=400)
        
        if not first_name:
          return JsonResponse({'error': 'Must provide First Name!'}, status=400)
        
        if not last_name:
          return JsonResponse({'error': 'Must provide Last Name!'}, status=400)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        
        if not password or not confirmation:          
          return JsonResponse({'error': 'Must provide password and confirmation!'}, status=400)
        
        if password != confirmation:
            return JsonResponse({'error': 'Passwords must match!'}, status=400)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            profile = UserProfile.objects.create(pk=user.id)
        
            profile.bio = ''
            profile.instagram_url = ''
            profile.facebook_url = ''
            profile.twitter_url = ''
            profile.linkedin_url = ''
            
            profile.save()
            
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        login(request, user)
        return JsonResponse({'message': 'Succesfully signed up.'}, status=200)
    else:
        return render(request, 'events/404.html')
    
  
@login_required
def profile(request, username):
    if not request.user.is_authenticated:
        return render(request, 'events/404.html')

    profile_user = User.objects.get(username=username)
    groups = Group.objects.filter(members__in=[profile_user])
    
    try:
      profile = UserProfile.objects.get(pk=profile_user.id)
      
      return render(request, 'events/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'groups': groups
        })
    except User.DoesNotExist:
      pass    
    
    return render(request, 'events/profile.html', {
        'profile_user': profile_user,
        'groups': groups
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
    # print(groups)

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
    if not group_description:
      return JsonResponse({'error': 'Please enter a group description.'}, status=400)
    
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
  

@csrf_exempt  
@login_required
def edit_group(request, group_id):
  if request.method == "PUT":
    data = json.loads(request.body)
    user = request.user
    group_name = data.get('name')
    group_description = data.get('description')
    privacy_setting = data.get('privacy_setting')
    image_url = data.get('image_url')
    
    if not group_name:
      return JsonResponse({'error': 'Please enter a group name.'}, status=400)
    if not group_description:
      return JsonResponse({'error': 'Please enter a group description.'}, status=400)
    
    try:
      group = Group.objects.get(pk=group_id)
      
      # Check if the user is the owner of the group
      if not group.owner == user:
        return JsonResponse({'error': 'You are not authorized to edit this group.'}, status=403)
      
      group.name = group_name
      group.description = group_description
      group.privacy_setting = privacy_setting # Use existing setting if not provided
      group.image_url = image_url
      group.save()
      
      # Success response
      return JsonResponse({'message': 'Group details updated successfully!', 'group': {
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'privacy_setting': group.privacy_setting
      }}, status=200)
    except Group.DoesNotExist:
      return JsonResponse({'error': 'Group not found.'}, status=404)
    except Exception as e: 
      return JsonResponse({'error': 'Failed to update group details.'}, status=500)
  else:
    return JsonResponse({'error': 'Invalid request!'}, status=400)
  
  
@csrf_exempt  
@login_required
def edit_profile(request, username):
  if request.method == "PUT":    
    try:
      profile_user = User.objects.get(username=username)
      user = request.user
      
      # Check if the user is updating their own profile
      if not profile_user == user:
        return JsonResponse({'error': 'You are not authorized to edit this profile!'}, status=403)
      
      
      data = json.loads(request.body)
      first_name = data.get('first_name')
      last_name = data.get('last_name')
      bio = data.get('bio')
      instagram_url = data.get('instagram_url')
      facebook_url = data.get('facebook_url')
      twitter_url = data.get('twitter_url')
      linkedin_url = data.get('linkedin_url')
      
      
      if not first_name:
        return JsonResponse({'error': 'Must provide First Name!'}, status=400)
      
      if not last_name:
        return JsonResponse({'error': 'Must provide Last Name!'}, status=400)
      
      profile_user.first_name = first_name
      profile_user.last_name = last_name
      
      
      profile = UserProfile.objects.get(pk=profile_user.id)
        
      print(profile)
        
      profile.bio = bio
      profile.instagram_url = instagram_url
      profile.facebook_url = facebook_url
      profile.twitter_url = twitter_url
      profile.linkedin_url = linkedin_url
      
      profile_user.save()
      profile.save()
      
      # Success response
      return JsonResponse({'message': 'Profile details updated successfully!', 'user': {
        'id': profile_user.id,
        'username': profile_user.username
      }}, status=200)
    except User.DoesNotExist:
      return JsonResponse({'error': 'User not found.'}, status=404)
    except Exception as e: 
      return JsonResponse({'error': 'Failed to update user profile.', 'errorMessage': str(e)}, status=500)
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
    event_category = request.POST.get('category') 
    event_group = request.POST.get('group')

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
          category_id=event_category,  
          host=user,  
          image=event_image,
      )
      if event_group:
        event.group_id = event_group
      if event_capacity:        
        event.capacity=event_capacity
      event.save()
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
  
  
@login_required
def groups(request):
  if request.method == "GET":
    user = request.user
    groups = Group.objects.filter(members__in=[user])
    groups_data = []
    for group in groups:
      groups_data.append({
        'id': group.id,
        'name': group.name,
      })
    return JsonResponse({'groups': groups_data}, status=200)
  else:
    return JsonResponse({'error': 'Invalid request method. Use GET.'}, status=400)

  
def get_users_not_in_group(request, group_id):
  if request.method != 'GET':
    return JsonResponse({'error': 'Invalid request method. Use GET.'}, status=400)
      
  try:
    group = Group.objects.get(pk=group_id)
  except Group.DoesNotExist:
    return JsonResponse({'error': 'Group with id %d does not exist.' % group_id}, status=400)

  all_users = User.objects.all()
  group_members = group.members.all()
  users_not_in_group = [user for user in all_users if user not in group_members]

  user_data = [{'id': user.id, 'username': user.username} for user in users_not_in_group]
  return JsonResponse({ 'users': user_data}, status=200)


@csrf_exempt
@login_required
def add_user_to_group(request, group_id):
  if request.method != 'POST':
    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)
      
  try:
    group = Group.objects.get(pk=group_id)
  except Group.DoesNotExist:
    return JsonResponse({'error': 'Group with id %d does not exist.' % group_id}, status=400)
  
  if not group.owner == request.user:
    return JsonResponse({'error': 'You are not authorized to edit this group.'}, status=403)

  data = json.loads(request.body)
  usernames = data.get('usernames', [])
  
  # Validate usernames (replace with your validation logic)
  valid_users = []
  for username in usernames:
    user = User.objects.filter(username=username).first()  # Check if user exists
    if user:
      valid_users.append(user)
    else:
      return JsonResponse({'error': 'User "%s" does not exist.' % username}, status=400)

  with transaction.atomic():
    try:
      group.members.add(*valid_users)  # Add users using bulk add
    except Exception as e:
      return JsonResponse({'error': 'Failed to add users to the group.', 'error_message': str(e)}, status=500)  
    
  return JsonResponse({ 'message': 'Succesfully added users to the group'}, status=200)


@login_required
@csrf_exempt
def delete_member_from_group(request, group_id):
  if request.method != 'DELETE':
    return JsonResponse({'error': 'Invalid request method. Use DELETE.'}, status=400)

  try:
    group = Group.objects.get(pk=group_id)
  except Group.DoesNotExist:
    return JsonResponse({'error': 'Group does not exist.'}, status=400)
  
  # Check permission
  if not group.owner == request.user:
    return JsonResponse({'error': 'You are not authorized to remove members from this group.'}, status=403)

  if not request.body:
    return JsonResponse({'error': 'Missing data in request body.'}, status=400)

  data = json.loads(request.body)
  member_id = data.get('memberId')

  try:
    member_to_remove = User.objects.get(pk=member_id)
  except User.DoesNotExist:
    return JsonResponse({'error': 'Member does not exist.'}, status=400)
  

  # Remove member from the group
  group.members.remove(member_to_remove)

  return JsonResponse({'message': 'Member successfully removed from the group.'}, status=200)


@login_required
@csrf_exempt
def edit_event(request, event_id):
  if request.method == 'PUT':
    try:
      data = json.loads(request.body)
      event = Event.objects.get(pk=event_id)  # Get the event object by ID

      title = data.get('title')
      description = data.get('description')
      date = data.get('date')
      time = data.get('time')
      location = data.get('location')
      category = data.get('category')
      capacity = data.get('capacity')
      image_url = data.get('image_url')

      # Basic validation
      if not title:
        return JsonResponse({'error': 'Please enter a title for the event.'}, status=400)
      if not description:
        return JsonResponse({'error': 'Please enter a description for the event.'}, status=400)

      # Update event details
      event.title = title
      event.description = description
      event.date = date
      event.time = time
      event.location = location
      
      if category:
        event.category_id = category
        
      if capacity:
        event.capacity = capacity  
        
      if image_url:
        event.image = image_url

      event.save()

      # Success response with basic event data
      return JsonResponse({'message': 'Event details updated successfully!', 'event': {
        'id': event.id,
      }}, status=200)

    except ObjectDoesNotExist:
      return JsonResponse({'error': 'Event not found.'}, status=404)
    except Exception as e: 
      return JsonResponse({'error': 'Failed to update event details.', 'error_message': str(e)}, status=500)
  else:
    return JsonResponse({'error': 'Invalid request! Use PUT.'}, status=400)