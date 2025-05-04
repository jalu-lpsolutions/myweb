from django import forms
from django.forms import ModelForm
from .models import Customer




class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["cif", "nombre", "apellido1", "apellido2", "telefono", "movil", "email", "customer_type", "direccion", "codigo_postal", "poblacion", "municipio", "provincia"]

class FilterCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["cif", "customer_type", "provincia"]
    def __init__(self, *args, **kwargs):
        super(FilterCustomerForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


