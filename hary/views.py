from django.shortcuts import render
from .models import Activity, Event

# Create your views here.
def home(request):
    activities = Activity.objects.all()
    events = Event.objects.all()
    context = {"activities": activities, "events": events}
    return render(request, 'hary/index.html', context=context)
