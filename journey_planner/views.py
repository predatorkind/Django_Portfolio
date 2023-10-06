from django.shortcuts import render
from journey_planner.models import Journey

# Create your views here.
def journey_planner(request):
    journeys = Journey.objects.all()

    context = {
        'journeys': journeys,

    }

    return render(request, "jp_main.html", context)