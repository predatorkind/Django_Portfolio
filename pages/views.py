from django.shortcuts import render
from pages.models import (Skill, Accomplishment, Education, Education_Detail, Job_Title, Employment,
                          Company, Location, Link, ProfileDetails)

def pool(request):
    return render(request, "pool.html")


def about_me(request):
    skills = Skill.objects.all()
    accomplishments = Accomplishment.objects.all()
    education = Education.objects.all()
    employment = Employment.objects.all().order_by('-id')
    links  = Link.objects.all()
    profile_details = ProfileDetails.objects.first()
    context = {
        "skills": skills,
        "accomplishments": accomplishments,
        "education": education,
        "employment": employment,
"links": links,
        "profile": profile_details,

    }
    return render(request, "about_me.html", context)


def links(request):
    return render(request, "links.html")
