from django import forms
from .models import Orden, Orden_Producto, Inventario, Producto, Proveedor, Almacen, Destino, Prod_Dest, Cliente
from django.utils import timezone
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserForm(UserCreationForm):
    
    rol_selector = forms.ChoiceField(label="Rol en el sistema",choices=[('empleado', 'Empleado'), ('gerente', 'Gerente'), ('ceo', 'CEO')])
    
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        

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
        widget=forms.DateInput(attrs={'class':'form-control','type': 'date', }),

    )
    fecha_requisicion = forms.DateField(
        label='Fecha de Requisición',
        required=False,
        localize=True,
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
    

    prod_image = forms.ImageField(label='Imagen del producto', required=False)
    nombre_producto = forms.CharField(label='Nombre del producto')
    cod_producto = forms.CharField(label="Codigo del producto")
    def clean(self):
        cleaned_data = super().clean()
        cant_min = cleaned_data.get('cant_min')
        cant_max = cleaned_data.get('cant_max')


        if cant_max <= cant_min:
            raise forms.ValidationError("La cantidad máxima debe ser mayor que la cantidad mínima.")
    class Meta:
        model = Producto
        fields = ["cod_producto","nombre_producto", "descripcion_prod","cant_min", "cant_max","id_proveedor", "prod_image"]
        

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
    tlf_proveedor = forms.CharField(
        label='Telefono',
        max_length=12,
        required=False  # Si no quieres que sea obligatorio
    )
    def clean_tlf_proveedor(self):
        telefono = self.cleaned_data['tlf_proveedor']
        if telefono:
            if not re.match(r'^\d{11}$', telefono):
                raise forms.ValidationError('Ingrese un número de teléfono válido en formato local (11 dígitos).')
        return telefono
    def clean_correo(self):
        email = self.cleaned_data['correo']
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if email:
            if not re.match(regex, email):
                raise forms.ValidationError('Por favor, ingresa una dirección de correo electrónico válida.')
        return email

class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields='__all__'
class ProdDestForm(forms.ModelForm):
    class Meta:
        model = Prod_Dest
        fields='__all__'
    fecha_ult_sumin = forms.DateField(
        label='Fecha ultimo suministro',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class AlmacenForm(forms.ModelForm):
    class Meta: 
        model = Almacen
        fields = '__all__'
    

class ClientesForm(forms.ModelForm):
    class Meta: 
        model = Cliente
        fields= '__all__'
    telefono = forms.CharField(
        label='Telefono 1',
        max_length=12,
        required=False  # Si no quieres que sea obligatorio
    )
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if telefono:
            if not re.match(r'^\d{11}$', telefono):
                raise forms.ValidationError('Ingrese un número de teléfono válido en formato local (11 dígitos).')
        return telefono
    def clean_correo(self):
        email = self.cleaned_data['correo']
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if email:
            if not re.match(regex, email):
                raise forms.ValidationError('Por favor, ingresa una dirección de correo electrónico válida.')
        return email
    
    telefono2 = forms.CharField(
        label='Telefono 2',
        max_length=12,
        required=False  # Si no quieres que sea obligatorio
    )
    def clean_telefono2(self):
        telefono2 = self.cleaned_data['telefono2']

        if telefono2:
            if not re.match(r'^\d{11}$', telefono2):
                raise forms.ValidationError('Ingrese un número de teléfono válido en formato local (11 dígitos).')
        return telefono2
    def clean_rif(self):
        rif = self.cleaned_data['rif']

        # Eliminar espacios y convertir a mayúsculas
        rif = rif.strip().upper()

        # Expresiones regulares para diferentes tipos de RIF
        cedula_venezolana = re.compile(r'^V-?(\d{9})$')
        cedula_extranjera = re.compile(r'^E-?(\d{8})$')
        rif_empresa = re.compile(r'^J-?(\d{9})$')

        # Validar el formato
        if not (cedula_venezolana.match(rif) or cedula_extranjera.match(rif) or rif_empresa.match(rif)):
            raise forms.ValidationError("El RIF ingresado no tiene un formato válido (Ejemplos: J-000950369 o V8765123).")
        return rif
    