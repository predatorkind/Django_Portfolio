from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from journey_planner.models import Journey
from django.db import models
from bootstrap_datepicker_plus.widgets import DateTimePickerInput



class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DateInput(forms. DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'

class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None):
        widgets = (DateInput(), TimeInput())
        forms.MultiWidget.__init__(self, widgets, attrs)

class EditJourneyForm(forms.ModelForm):
    id = models.IntegerField()
    end_date = forms.SplitDateTimeField(widget=SplitDateTimeWidget)
    start_date = forms.SplitDateTimeField(widget=SplitDateTimeWidget, required=True)

    class Meta:
        model = Journey
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",

                  ]


