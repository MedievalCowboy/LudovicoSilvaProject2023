from django import forms
from .models import Orden, Orden_Producto, Inventario, Producto, Proveedor, Almacen, Destino, Prod_Dest, Cliente, Profile
from django.utils import timezone
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .security.utils import obtener_rol_mas_alto
from .security.hierarchy import get_allowed_roles, DISPLAY_NAMES

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'nombres', 
            'apellidos', 
            'telefono', 
            'telefono2', 
            'cedula', 
            'email', 
            'estado', 
            'direccion', 
            'cargo', 
            'tema_sistema', 
            'image'
        ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'tema_sistema': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserForm(UserCreationForm):
    rol_selector = forms.ChoiceField(
        label="Rol en el sistema",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        # Extraer el request del kwargs
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Configurar opciones dinámicas del rol
        if self.request and self.request.user.is_authenticated:
            current_role = obtener_rol_mas_alto(self.request.user)
            allowed_roles = get_allowed_roles(current_role)
            
            
            self.fields['rol_selector'].choices = [
                (role, DISPLAY_NAMES.get(role, role.capitalize()))
                for role in allowed_roles
                if role != 'admin' or self.request.user.is_superuser
            ]

        # Estilos para todos los campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = '' 

class OrdenForm(forms.ModelForm):

    # Definir las opciones para el campo "Estado"
    ESTADO_CHOICES = (
        ('Por aprobar', 'Por aprobar'),
        ('Tramitando', 'Tramitando'),
        ('Finalizado', 'Finalizado'),
    )

    class Meta:
        model = Orden
        fields = [
            'num_orden',
            'id_cliente',
            'id_destino',
            'estado',
            'desc_requisicion',
            'fecha_requisicion',
            'fecha_emision',
            'fecha_entrega',
            'num_factura',
            'solicitado',
            'tlf_solicitado',
            'num_lote',
        ] # Lista de campos en el orden deseado
        exclude = ('id_usuario', 'fecha_ult_mod', 'creado_en', 'num_factura') 

        # Personalización de campos de fecha
    fecha_emision = forms.DateField(
        label='Fecha de Emisión',
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','type': 'date', }),

    )
    fecha_requisicion = forms.DateField(
        label='Fecha de Requisición',
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','type': 'date', }),
    )
    fecha_entrega = forms.DateField(
        label='Fecha de Entrega',
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','type': 'date', }),
    )
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, label='Estado de la Orden', widget=forms.Select(attrs={'class': 'form-control'})) # Label personalizado para Estado

    tlf_solicitado = forms.CharField(
        label='Teléfono del Solicitante',
        max_length=12,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    num_orden = forms.IntegerField(
        label='Número de Orden', 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    #num_factura = forms.CharField(
    #    label='Número de Factura',
    #    max_length=20,
    #    help_text="Formato de factura: F01-YYYYNUMORDEN (Ej: F01-2025000001)", 
    #    widget=forms.TextInput(attrs={'class': 'form-control'})
    #)
    desc_requisicion = forms.CharField(
        label='Descripción de la Requisición', 
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    solicitado = forms.CharField(
        label='Nombre del Solicitante', 
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    num_lote = forms.CharField(
        label='Número de Lote', 
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    id_cliente = forms.ModelChoiceField(
        queryset=Orden.id_cliente.field.related_model.objects.all(),
        label='Cliente', 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    id_destino = forms.ModelChoiceField(
        queryset=Orden.id_destino.field.related_model.objects.all(),
        label='Destino de la Orden', 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


    def clean_tlf_solicitado(self):
        tlf_solicitado = self.cleaned_data.get('tlf_solicitado')
        if tlf_solicitado and not re.match(r'^\d{11}$', tlf_solicitado):
            raise forms.ValidationError('Ingrese un número de teléfono válido en formato local (11 dígitos).')
        return tlf_solicitado

    def clean_num_factura(self):
        num_factura = self.cleaned_data.get('num_factura')
        if num_factura: # Solo validar si se ha ingresado un valor
            if not re.match(r'^[A-Za-z0-9]{3}-\d{8}$', num_factura):
                raise forms.ValidationError(f'Ingrese un número de factura válido con el formato: F01-YYYYNUMORDEN (Ej: F01-2025000001). Formato esperado: XXX-YYYYNNNNNNNN')
        return num_factura
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_requisicion = cleaned_data.get('fecha_requisicion')
        fecha_entrega = cleaned_data.get('fecha_entrega')

        if fecha_requisicion and fecha_emision and fecha_emision < fecha_requisicion:
            self.add_error('fecha_emision', 'La Fecha de Emisión debe ser posterior a la Fecha de Requisición.')

        if fecha_requisicion and fecha_entrega and fecha_entrega <= fecha_requisicion:
            self.add_error('fecha_entrega', 'La Fecha de Entrega debe ser posterior a la Fecha de Requisición.')

        if fecha_emision and fecha_entrega and fecha_entrega <= fecha_emision:
            self.add_error('fecha_entrega', 'La Fecha de Entrega debe ser posterior a la Fecha de Emisión.')

        if fecha_requisicion and fecha_entrega and fecha_requisicion >= fecha_entrega: 
            self.add_error('fecha_requisicion', 'La Fecha de Requisición debe ser anterior a la Fecha de Entrega.')


        return cleaned_data


class OrdenProductoForm(forms.ModelForm):
    EMPAQUE_CHOICES = [
        ('Caja', 'Caja'),
        ('Bolsa', 'Bolsa'),
        ('Bulto', 'Bulto'),
        ('Tambor', 'Tambor'),
        ('Granel', 'Granel'),
        ('Palet', 'Palet'),
        ('Bidón', 'Bidón'),
        ('Saco', 'Saco'),
    ]
    
    empaque = forms.ChoiceField(
        choices=EMPAQUE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Orden_Producto
        fields = ["id_orden", "producto", "cantidad", "precio_unit", "empaque"]
        
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)
        if pk:
            self.fields['id_orden'].initial = pk
        self.fields['id_orden'].disabled = True


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto', 'precio_unit_ref', 'cant_disponible', 'id_almacen', 'nota', 'tipo_movimiento']
        widgets = {
            'tipo_movimiento': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.fields['tipo_movimiento'].initial = 'ENTRADA'
        if 'instance' in kwargs:
            self.fields['tipo_movimiento'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        cant_disponible = cleaned_data.get('cant_disponible')
        producto = cleaned_data.get('producto')

        if cant_disponible is not None and producto:
            if cant_disponible < producto.cant_min or cant_disponible > producto.cant_max:
                raise forms.ValidationError("La cantidad debe estar dentro de los límites max-min del producto.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.fecha_ult_mod_inv = timezone.now()
        if commit:
            instance.save()
        return instance



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
        required=False
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
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','type': 'date', }),
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
        required=False 
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
        required=False
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
    