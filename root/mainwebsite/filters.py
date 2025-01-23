# filters.py
import django_filters
from django import forms
from .models import LoginHistory

class LoginHistoryFilter(django_filters.FilterSet):
    user__username = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por usuario...'})
    )
    
    timestamp_range = django_filters.DateFromToRangeFilter(
        field_name='timestamp',
        label='Rango de fechas',
        widget=django_filters.widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'datepicker'
        })
    )
    
    event_type = django_filters.ChoiceFilter(
        choices=LoginHistory._meta.get_field('event_type').choices,
        empty_label='Todos los eventos',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = LoginHistory
        fields = [] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Orden personalizado de los campos
        self.filters = {
            'user__username': self.filters['user__username'],
            'timestamp_range': self.filters['timestamp_range'],
            'event_type': self.filters['event_type']
        }
