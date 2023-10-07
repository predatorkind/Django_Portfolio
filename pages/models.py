from django.db import models

class Skill(models.Model):
    description = models.CharField(max_length=100)


class Accomplishment(models.Model):
    description = models.CharField(max_length=150)
    url = models.CharField(max_length=150, blank=True)


class Education(models.Model):
    school = models.CharField(max_length=80)
    duration = models.CharField(max_length=40)
    details = models.TextField()


class Education_Detail(models.Model):
    details = models.CharField(max_length=200)
    school = models.ForeignKey(Education, on_delete=models.CASCADE, related_name="edudets")


class Job_Title(models.Model):
    name = models.CharField(max_length=50)


class Company(models.Model):
    name = models.CharField(max_length=50)


class Location(models.Model):
    name = models.CharField(max_length=50)


class Employment(models.Model):
    title = models.ForeignKey(Job_Title, on_delete=models.CASCADE, related_name="job")
    duration = models.CharField(max_length=40)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location")

class Employment_Details(models.Model):
    details = models.CharField(max_length=200)
    employment = models.ForeignKey(Employment, on_delete=models.CASCADE, related_name="empldets")


class Link(models.Model):
    description = models.CharField(max_length=40)
    url = models.CharField(max_length=300)


class ProfileDetails(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    email =models.CharField(max_length=30)
    description = models.CharField(max_length=500)


def get_models():
    return ['skill',
            'profiledetails',
            'link',
            'location',
            'education_detail',
            'employment_details',
            'employment',
            'accomplishment',
            'education',
            'job_title',
            'company',
            ]