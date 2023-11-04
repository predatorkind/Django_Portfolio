from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from journey_planner.models import Journey, Journey_Point
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
    start_date = forms.SplitDateTimeField(widget=SplitDateTimeWidget(attrs={"time_format":'%H:%M'}), required=True)

    class Meta:
        model = Journey
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",

                  ]

    def clean(self):
        cleaned_data = super().clean()
        s_date = cleaned_data.get('start_date', '')
        e_date = cleaned_data.get('end_date', '')

        if e_date < s_date:
            data = cleaned_data.copy()
            data["end_date"] = data["start_date"]
            return  data
        # if e_date < s_date:
        #     msg = "End Date has to be later than Start Date!"
        #     raise forms.ValidationError(msg)
        return cleaned_data

class EditPointForm(forms.ModelForm):
    id = models.IntegerField()
    end_date = forms.SplitDateTimeField(widget=SplitDateTimeWidget)
    start_date = forms.SplitDateTimeField(widget=SplitDateTimeWidget, required=True)
    is_selected = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'width:30px;height:30px;margin-top:10px;'}), label="", required=False)

    class Meta:
        model = Journey_Point
        fields = [
            "id",
            "name",
            "description",
            "status",
            "is_selected",
            "start_date",
            "end_date",
            "address",
            "cost",
            "place_url",
            "maps_url",

                  ]

    def clean(self):
        cleaned_data = super().clean()
        s_date = cleaned_data.get('start_date', '')
        e_date = cleaned_data.get('end_date', '')

        if e_date < s_date:
            data = cleaned_data.copy()
            data["end_date"] = data["start_date"]
            return  data

        # if e_date< s_date:
        #     msg = "End Date has to be later than Start Date!"
        #     raise forms.ValidationError(msg)
        return cleaned_data


