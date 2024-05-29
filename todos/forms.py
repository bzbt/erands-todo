from django import forms

from todos.models import Task, Location, Weather


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks.

    Fields:
    - title: The title of the task
    - description: The description of the task
    - location: The location of the task
    """
    class Meta:
        model = Task
        fields = ["title", "description", "location"]
        labels = {
            "title": "Title",
            "description": "Description",
            "location": "Location",
        }

    weather = forms.JSONField(widget=forms.HiddenInput(), required=False)
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(), empty_label='-- Select location --', required=True,
    )

    def __init__(self, *args, **kwargs):
        disable_all = kwargs.pop('disable_all', False)
        super(TaskForm, self).__init__(*args, **kwargs)

        if disable_all:
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True
        if self.instance and self.instance.weather:
            self.fields['weather'].initial = self.instance.weather.as_dictionary()


class WeatherForm(forms.ModelForm):
    """
    Form for creating and updating weather, as part of Task form.

    This form is hidden and is populated by JavaScript, based on the location selected.

    Fields:
    - temperature: The temperature in Kelvin
    - humidity: The humidity in percentage
    - condition: The weather condition
    - latitude: The latitude of the location
    - longitude: The longitude of the location
    """
    class Meta:
        model = Weather
        fields = ['temperature', 'humidity', 'condition', 'latitude', 'longitude']

