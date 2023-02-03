from django import forms
from django_filters import FilterSet, AllValuesFilter, MultipleChoiceFilter, IsoDateTimeFilter
from django_filters import DateTimeFilter, NumberFilter

from .models import Event

TYPE_EVENT = ['TypeA', 'TypeB', 'TypeC']
TYPE_EVENT_CHOICES = sorted([(item, item) for item in TYPE_EVENT])

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class EventFilter(FilterSet):
    from_created_at_date = IsoDateTimeFilter(field_name='created_at',
                                          lookup_expr='gte',
                                             widget=DateTimeInput()
                                             )
    to_created_at_date = IsoDateTimeFilter(field_name='created_at',
                                        lookup_expr='lte',
                                           widget=DateTimeInput()
                                           )
    type_event_choise = MultipleChoiceFilter(field_name='type_event', choices= TYPE_EVENT_CHOICES)

    class Meta:
        model = Event
        fields = (
            'from_created_at_date',
            'to_created_at_date',
            'type_event_choise',

        )
