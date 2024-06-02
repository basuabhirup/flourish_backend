from django.shortcuts import render
from .models import Event


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