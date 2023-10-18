from django import forms
from .models import Orden, Orden_Producto
import re




class OrdenForm(forms.ModelForm):

    # Definir las opciones para el campo "Estado"
    ESTADO_CHOICES = (
        ('En espera', 'En espera'),
        ('Finalizado', 'Finalizado'),
        ('Tramitando', 'Tramitando'),
    )

    class Meta:
        model = Orden
        fields = '__all__'
        exclude = ('id_usuario',)

       # Personalización de campos de fecha
    fecha_emision = forms.DateField(
        label='Fecha de Emisión',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_requisicion = forms.DateField(
        label='Fecha de Requisición',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_entrega = forms.DateField(
        label='Fecha de Entrega',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, label='Estado')

    tlf_solicitado = forms.CharField(
        label='Teléfono Solicitado',
        max_length=12,
        required=False  # Si no quieres que sea obligatorio
    )

    

    def clean_tlf_solicitado(self):
        tlf_solicitado = self.cleaned_data['tlf_solicitado']
        if not re.match(r'^\d{11}$', tlf_solicitado):
            raise forms.ValidationError('Ingrese un número de teléfono válido en formato local (11 dígitos).')
        return tlf_solicitado



class OrdenProductoForm(forms.ModelForm):
    class Meta:
        model = Orden_Producto
        fields = ['id_orden', 'cantidad', 'precio_unit','empaque', 'producto', ]
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk',None)
        super(OrdenProductoForm,self).__init__(*args,**kwargs)
        if pk:
            
            self.fields['id_orden'].initial = pk
            #self.fields['id_orden'].widget = forms.HiddenInput()
            self.fields['id_orden'].disabled = True