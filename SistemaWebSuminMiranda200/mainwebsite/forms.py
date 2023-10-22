from django import forms
from .models import Orden, Orden_Producto, Inventario, Producto, Proveedor, Almacen, Destino, Prod_Dest
from django.utils import timezone
import re




class OrdenForm(forms.ModelForm):

    # Definir las opciones para el campo "Estado"
    ESTADO_CHOICES = (
        ('Por aprobar', 'Por aprobar'),
        ('Tramitando', 'Tramitando'),
        ('Finalizado', 'Finalizado'),
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
        fields = ["id_orden", "producto", "cantidad", "precio_unit", "empaque"]
        
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super(OrdenProductoForm, self).__init__(*args, **kwargs)
        if pk:
            self.fields['id_orden'].initial = pk

        # Establecer el campo 'id_orden' como no editable
        self.fields['id_orden'].disabled = True


from django import forms
from .models import Inventario

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto','precio_unit_ref','cant_inicial','cant_disponible', 'id_almacen', 'nota']
        
        
    def clean(self):
        cleaned_data = super().clean()
        cant_inicial = cleaned_data.get('cant_inicial')
        cant_disponible = cleaned_data.get('cant_disponible')
        producto = cleaned_data.get('producto')

        if self.instance.pk and cant_disponible > cant_inicial:
            raise forms.ValidationError("La cantidad disponible no puede ser mayor que la inicial.")

        if cant_inicial < producto.cant_min or cant_inicial > producto.cant_max:
            raise forms.ValidationError("La cantidad inicial debe estar dentro de los límites max-min del producto.")

    def save(self, commit=True):
        instance = super(InventarioForm, self).save(commit=False)
        instance.fecha_ult_mod_inv = timezone.now()
        if not self.instance.pk:
            instance.cant_disponible = instance.cant_inicial
        if commit:
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields.pop('cant_disponible',None)



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        cant_min = cleaned_data.get('cant_min')
        cant_max = cleaned_data.get('cant_max')


        if cant_max <= cant_min:
            raise forms.ValidationError("La cantidad máxima debe ser mayor que la cantidad mínima.")
        

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields='__all__'


class ProdDestForm(forms.ModelForm):
    class Meta:
        model = Prod_Dest
        fields='__all__'