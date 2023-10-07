from django.shortcuts import render, redirect
from journey_planner.models import Journey
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("journey_planner")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})

# Create your views here.
def journey_planner(request):
    journeys = Journey.objects.all()

    context = {
        'journeys': journeys,

    }

    return render(request, "jp_main.html", context)