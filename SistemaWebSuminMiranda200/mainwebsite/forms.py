from django import forms
from .models import Orden, Orden_Producto

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = '__all__'

    # Personalización de etiquetas
    labels = {
        'num_orden': 'Número de Orden',
        'fecha_emision': 'Fecha de Emisión',
        'estado': 'Estado',
        'num_factura': 'Número de Factura',
        'desc_requisicion': 'Descripción de la Requisición',
        'fecha_requisicion': 'Fecha de Requisición',
        'fecha_entrega': 'Fecha de Entrega',
        'solicitado': 'Solicitado por',
        'tlf_solicitado': 'Teléfono del Solicitado',
        'fecha_ult_mod': 'Fecha de Última Modificación',
        'num_lote': 'Número de Lote',
        'id_cliente': 'Cliente',
        'id_destino': 'Destino',
        'id_usuario': 'Usuario',
    }

    # Personalización de widgets para campos de fecha
    widgets = {
        'fecha_emision': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        'fecha_requisicion': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        'fecha_entrega': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        'fecha_ult_mod': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
    }

class OrdenProductoForm(forms.ModelForm):
    class Meta:
        model = Orden_Producto
        fields = ['id_orden', 'cantidad', 'precio_unit','empaque', 'producto', ]
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk',None)
        super(OrdenProductoForm,self).__init__(*args,**kwargs)
        if pk:
            print("FUNCIONANDOOOOO")
            self.fields['id_orden'].initial = pk
            #self.fields['id_orden'].widget = forms.HiddenInput()
            self.fields['id_orden'].disabled = True