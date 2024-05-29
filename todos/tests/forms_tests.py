from django.forms import ModelChoiceField, JSONField

from todos.forms import TaskForm
from todos.models import Weather


def test_task_form():
    form = TaskForm()
    assert form.fields['title'].label == "Title"
    assert form.fields['description'].label == "Description"
    assert isinstance(form.fields['location'], ModelChoiceField)
    assert isinstance(form.fields['weather'], JSONField)

def test_task_form_disable_all():
    form = TaskForm(disable_all=True)
    for field in form.fields:
        assert form.fields[field].widget.attrs['disabled'] == True

def test_task_form_initial_weather():
    form = TaskForm(instance=TaskForm.Meta.model())
    assert form.fields['weather'].initial is None
    form = TaskForm(instance=TaskForm.Meta.model(weather=Weather(
        temperature=0.0, humidity=0.0, condition=200, latitude=0.0, longitude=0.0
    )))
    assert form.fields['weather'].initial == form.instance.weather.as_dictionary()
