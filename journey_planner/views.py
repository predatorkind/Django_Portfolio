from django.shortcuts import render, redirect
from journey_planner.models import Journey, User_Journey, Journey_Point, Status
from .forms import NewUserForm, EditJourneyForm, EditPointForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
from typing import List, Tuple
import googlemaps
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import ssl
import urllib.request
import urllib.parse
import urllib.error


def get_dates_list(journey: Journey) -> List:
    dates=[]
    if journey:
            td = journey.end_date - journey.start_date
            print(f"Time delta: {td} / {td.days} days.")
            num_days =  td.days + 1
            if td.days < 1 and journey.start_date.date() != journey.end_date.date():
                num_days += 1
            print(f"the trip is {num_days} long.")
            date = journey.start_date.date()
            for d in range(num_days):
                dates.append(date)
                date = date + timedelta(days=1)
            print(dates)

    return dates


def get_assigned_points(journey: Journey) -> List:
    points = []
    if journey:
        for p in journey.journey_point_set.all().order_by("start_date"):
            if p.is_selected:
                points.append(p)
    return points


def get_unassigned_points(journey: Journey) -> List:
    points = []
    if journey:
        for p in journey.journey_point_set.all().order_by("start_date"):
            if not p.is_selected:
                points.append(p)
    return  points


def get_total_cost(journey: Journey) -> str:
    if journey:
        cost = 0.0
        for p in journey.journey_point_set.all():
            if p.is_selected:
                cost += p.cost
    total = f"{cost:.2f}"
    print(total)
    return total


def get_location_old(address: str) -> Tuple:
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    api_key = settings.MAPS_API_KEY
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    params = dict()
    params['address'] = address
    params['key'] = api_key

    url = geocode_url + urllib.parse.urlencode(params)

    uhandle = urllib.request.urlopen(url, context=ctx)
    data = uhandle.read().decode()

    # print("Retrieved", len(data), "characters.")

    try:
        js = json.loads(data)

    except:
        js = None

    if not js or "status" not in js or js["status"] != "OK":
        print("Failed to retrieve data.")

        return 0, 0, ""

    else:

        # print(json.dumps(js, indent=4))

        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        name = js["results"][0]["formatted_address"]

        return lat, lng, name


def get_location(address: str) -> Tuple:

    api_key = settings.GEOCODE_KEY
    gmaps = googlemaps.Client(key=api_key)

    data = gmaps.geocode(address)


    print("Retrieved", len(data), "characters.")
    print(data)

    if len(data) > 0:

        lat = data[0]["geometry"]["location"]["lat"]
        lng = data[0]["geometry"]["location"]["lng"]
        name = data[0]["formatted_address"]

        return lat, lng, name

    else:
        return 0, 0, ""


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
                usr = User.objects.filter(id=u.user_id).first()
                if usr:
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
        assign_id = request.POST.get("assign_point")
        unassign_id = request.POST.get("unassign_point")
        plus_date_id = request.POST.get("plus_date")
        minus_date_id = request.POST.get("minus_date")

        journey = Journey.objects.filter(id=journey_id).first()
        dates = get_dates_list(journey)



        if assign_id and assign_id != "0":

            point = Journey_Point.objects.filter(id=assign_id).first()
            if point:
                if point.start_date >= journey.start_date and point.start_date <= journey.end_date:
                    point.is_selected = True
                    point.save()
                else:
                    messages.error(request, "Journey point start date is outside the journey schedule!")
        if unassign_id and unassign_id != "0":

            point = Journey_Point.objects.filter(id=unassign_id).first()
            if point:
                point.is_selected = False
                point.save()
        if plus_date_id and plus_date_id != "0":
            point = Journey_Point.objects.filter(id=plus_date_id).first()
            if point:
                if point.start_date.strftime("%d-%m-%Y") == request.POST.get("p_date"):
                    dat = point.start_date + timedelta(days=1)
                    if dat.date() <= journey.end_date.date():
                        point.start_date = point.start_date + timedelta(days=1)
                        point.end_date = point.end_date + timedelta(days=1)
                        point.save()
        if minus_date_id and minus_date_id != "0":
            point = Journey_Point.objects.filter(id=minus_date_id).first()
            if point:
                if point.start_date.strftime("%d-%m-%Y") == request.POST.get("p_date"):
                    if point.start_date - timedelta(days=1) >= journey.start_date:
                        point.start_date = point.start_date - timedelta(days=1)
                        point.end_date = point.end_date - timedelta(days=1)
                        point.save()






        context = {
            'journey': journey,
'cost': get_total_cost(journey),
            'dates': dates,
            'assigned': get_assigned_points(journey),
            'unassigned': get_unassigned_points(journey),

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
                journey = Journey(name="New Journey", start_date=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0), end_date=datetime.now().replace(hour=23,minute=59, second=0))
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


def edit_point(request):
    if request.user.is_authenticated:

        journey_id = request.POST.get("journey_id")
        print(f"Journey ID: X{journey_id}X)")
        point_id = request.POST.get("point_id")
        save_data = request.POST.get("save_data")
        delete_data = request.POST.get("delete_data")

        journey = Journey.objects.filter(id=journey_id).first()
        dates = get_dates_list(journey)


        if delete_data == "true":
            point = Journey_Point.objects.filter(id=point_id).first()
            if point:
                point.delete()

            ctx = {
                "journey": journey,
                "dates": dates,
                "cost": get_total_cost(journey),
                                "assign_id": 0,
                "unassign_id": 0,
                "plus_date_id": 0,
                "minus_date_id": 0,
                "assigned": get_assigned_points(journey),
                "unassigned": get_unassigned_points(journey)

            }
            return render(request,"view_journey.html", ctx)
        elif save_data == "true":
            point = Journey_Point.objects.filter(id=point_id).first()
            f = EditPointForm(request.POST, instance=point)
            if f.is_valid():
                f.save()
                ctx = {
                    "journey": journey,
                    "dates": dates,
                    "cost": get_total_cost(journey),
                    "assign_id": 0,
                    "unassign_id": 0,
                    "plus_date_id": 0,
                    "minus_date_id": 0,
                    "assigned": get_assigned_points(journey),
                    "unassigned": get_unassigned_points(journey),

                }
                return render(request, "view_journey.html", ctx)
            else:
                messages.error(request, "Some data provided are incorrect.")
                ctx = {
                    "journey": journey,
                    "point": point,
                    "form": f,
                }
                return  render(request, "edit_point.html", ctx)
        else:

            if point_id == "0":
                year = journey.start_date.year
                month = journey.start_date.month
                day = journey.start_date.day
                point = Journey_Point (name="New Point", start_date=datetime(year=year,month=month, day=day),
                                       end_date=datetime(year=year,month=month, day=day), journey_id=journey, status=Status.objects.get(id=1))

                point.save()

            else:

                point = Journey_Point.objects.filter(id=point_id).first()

            form = EditPointForm(instance=point)

            context = {
            'journey': journey,
                'point': point,
            'form': form,

        }

    else:
        messages.error(request, "You need to log in to use the Journey Planner.")

        return redirect("login")
    return render(request, "edit_point.html", context)

@ensure_csrf_cookie
def map_search(request):
    key = settings.MAPS_API_KEY
    if request.user.is_authenticated:
        journey_id = request.POST.get("journey_id")
        point_id = request.POST.get("point_id")
        save_data = request.POST.get("save_data")
        find_address = request.POST.get("find_address")
        clat = 0
        clng = 0
        map_data = {
            "center": {
                "lat": clat,
                "lng": clng,
                "address": "empty"
            },
            "points": []
        }


        if journey_id and journey_id != "0":
            journey = Journey.objects.filter(id=journey_id).first()
            if journey.location != "":
                clat, clng = journey.location.split("/")

            else:
                clat, clng, addr = get_location(journey.name)
                journey.location = str(clat) + "/" + str(clng)
                journey.save
                print(f"Journey after saving location: {journey.location}")
                print(f"***Obtained location: {clat} / {clng} / {addr}")

            map_data['center']['lat'] = float(clat)
            map_data['center']['lng'] = float(clng)
            map_data['center']['address'] = journey.name

        if point_id and point_id != "0":
            point = Journey_Point.objects.filter(id=point_id).first()
            if point.location != "":
                lat, lng = point.location.split("/")
                map_data['center']['lat'] = float(lat)
                map_data['center']['lng'] = float(lng)
                map_data['center']['address'] = point.address
                map_data['points'].append({
                    'lat': float(lat),
                    'lng': float(lng),
                    'address': point.address,
                    'name': point.name,
                })



            point_pk = point.id
        else:
            point_pk = 0
            point = 0
            if journey:
                for p in journey.journey_point_set.all():
                    if p.is_selected and p.location != "":
                        lat, lng = p.location.split("/")
                        map_data['points'].append({
                            'lat': float(lat),
                            'lng':float(lng),
                            'address': p.address,
                            'name': p.name,
                                                   })

        print(f"Center: {map_data['center']}")
        print(f"Points: {map_data['points']}")


        #map_data = json.dumps(map_data)






        context = {
            'journey': journey,
            'point': point,
            'point_pk': point_pk,
            'key': key,
            'map_data': map_data,

        }

    else:
        messages.error(request, "You need to log in to use the Journey Planner.")
        return redirect("login")

    return render(request, 'map_search.html', context)


def loc_data(request):
    print(request.POST)
    lat, lng, addr = get_location(request.POST.get('address'))
    name = "Not Found"
    if addr:
        if len(addr) > 10:
            name = addr[:10] + ".."
        else:
            name = addr[:10]

    if request.POST.get('save') == 'true':

        point = Journey_Point.objects.filter(id=request.POST.get('point')).first()
        if point:
            print("saving: " , point)
            point.address = addr
            point.location = str(lat) + "/" + str(lng)
            point.save()

        else:
            journey = Journey.objects.filter(id=request.POST.get('journey')).first()
            if journey:
                print("saving: ", journey)
                journey.location = str(lat) + "/" + str(lng)
                journey.save()

    map_data = {
        'center': {
            'lat': lat,
            'lng': lng,
            'address': addr
        },
        'points': [{'lat':lat, 'lng': lng, 'address': addr, 'name': name}]
    }

    return JsonResponse(map_data, safe=False)








