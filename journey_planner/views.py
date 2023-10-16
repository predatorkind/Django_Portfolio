from django.shortcuts import render, redirect
from journey_planner.models import Journey, User_Journey
from .forms import NewUserForm, EditJourneyForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
from typing import List


def get_dates_list(journey: Journey) -> List:
    dates=[]
    if journey.end_date > journey.start_date:
        td = journey.end_date - journey.start_date
        num_days =  td.days
        print(f"the trip is {num_days} long.")
        date = journey.start_date.date()
        for d in range(num_days + 1):
            dates.append(date)
            date = date + timedelta(days=1)
        print(dates)

    return dates


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("links")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


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


def logout_request(request):
    logout(request)

    return render(request=request, template_name="links.html")


def journey_planner(request):
    if request.method == "POST":
        extra_user = User.objects.filter(username=request.POST.get("extra_user")).first()
        # if no results send error message
        if extra_user is None:
            print("no such user")
            messages.error(request,"User not found.")
        else:
            journey = Journey.objects.filter(id=request.POST.get("journey_id")).first()
            user_journey = User_Journey(user_id=extra_user.id, journey_id=journey)
            user_journey.save()
            messages.success(request, f"User {extra_user.username} added to {journey.name}.")
    if request.user.is_authenticated:
        user_id = request.user.pk
        journeys = Journey.objects.filter(user_journey__user_id = user_id)
        users = User.objects.all()

        names = {}
        for j in journeys:
            for u in j.user_journey_set.all():
                username = User.objects.get(id=u.user_id).username
                if j.id in names:
                    names[j.id].append(username)
                else:
                    names[j.id] = [username]

        context = {
            'journeys': journeys,
'names':names,
        }
        # print("Dictionary", context)
    else:
        messages.error(request, "You need to log in to use the Journey Planner.")
        return redirect("login")

    return render(request, "jp_main.html", context)


def view_journey(request):
    if request.user.is_authenticated:
        journey_id = request.POST.get("journey_id")

        journey = Journey.objects.filter(id=journey_id).first()
        dates = get_dates_list(journey)
        for p in journey.journey_point_set.all():
            print(p)

        context = {
            'journey': journey,
            'dates': dates,

        }

    else:
        messages.error(request, "You need to log in to use the Journey Planner.")
        return redirect("login")

    return render(request, "view_journey.html", context)


def edit_journey(request):
    if request.user.is_authenticated:
        journey_id = request.POST.get("journey_id")
        save_data = request.POST.get("save_data")
        delete_data = request.POST.get("delete_data")
        if delete_data == "true":
            journey = Journey.objects.filter(id=journey_id).first()
            journey.delete()
            return redirect("journey_planner")
        elif save_data == "true":
            journey = Journey.objects.filter(id=journey_id).first()
            f = EditJourneyForm(request.POST, instance=journey)
            if f.is_valid():
                f.save()
                return redirect("journey_planner")
            else:
                messages.error(request, "Some data provided are incorrect.")
                ctx = {
                    "journey": journey,
                    "form": f,
                }
                return  render(request, "edit_journey.html", ctx)
        else:

            if journey_id == "0":
                journey = Journey(name="New Journey", start_date=datetime.now())
                journey.save()
                user_journey = User_Journey(user_id=request.user.pk,journey_id=journey)

                user_journey.save()
            else:

                journey = Journey.objects.filter(id=journey_id).first()

            form = EditJourneyForm(instance=journey)

            context = {
            'journey': journey,
            'form': form,

        }

    else:
        messages.error(request, "You need to log in to use the Journey Planner.")
        return redirect("login")

    return render(request, "edit_journey.html", context)