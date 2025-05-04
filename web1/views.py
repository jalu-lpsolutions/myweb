from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required,permission_required
from .forms import CustomerForm,FilterCustomerForm
from .models import Customer,Serial_number
import datetime
from django.core.exceptions import PermissionDenied
import os
import io
from io import BytesIO

# Create your views here.

def index2(request):
    return render(request, 'web1/index.html')


def check_credentials(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        #return redirect("/web1/customer_list")
        return redirect("/web1/customer_list/")
    else:
        #return redirect("/web1/index")
        return redirect("/accounts/login/")
        ...



@login_required
def index(request):
    return HttpResponse("SERVIDOR EN MARCHA.")




@login_required
def check_user(request, entidad_id,Entidad):
    entidad = Entidad.objects.get(id=entidad_id)
    print(entidad.user)
    print(request.user)
    if entidad.user != request.user:
        raise PermissionDenied

@login_required
def check_permission(request, entidad_id,Entidad):
    entidad = Entidad.objects.get(id=entidad_id)
    print(entidad.user)
    print(request.user)
    usuarios_permitidos = [request.user] + get_descendientes(request.user)
    if entidad.user not in usuarios_permitidos:
        raise PermissionDenied   

def get_descendientes(usuario):
    descendientes = []

    hijos_directos = User.objects.filter(perfilusuario__padre=usuario)
    for hijo in hijos_directos:
        descendientes.append(hijo)
        descendientes.extend(get_descendientes(hijo))  # recursivo

    return descendientes




@login_required
@permission_required('web1.view_customer')
def customer_list(request):
    CustomerFilterForm=FilterCustomerForm()
    
    clientes=Customer.objects.all()


    usuarios_visibles = [request.user] + get_descendientes(request.user)
    print(usuarios_visibles)
    clientes= Customer.objects.filter(user__in=usuarios_visibles)

    #clientes = clientes.filter(user_id=request.user)

    cif = request.GET.get('cif')
    if cif:
        clientes = clientes.filter(cif=cif)

    customer_type = request.GET.get('customer_type')
    if customer_type:
        clientes = clientes.filter(customer_type=customer_type)

    provincia = request.GET.get('provincia')
    if provincia:
        clientes = clientes.filter(provincia=provincia)

    
    table=clientes
    context = {"table":table,"CustomerFilterForm":CustomerFilterForm}
    return render(request, "web1/customer_list.html", context)


@login_required
def customer_form(request,customer_id):

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        customer = Customer.objects.get(id=customer_id)
        form = CustomerForm(request.POST,instance=customer)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            context={"form": form}
            return render(request, "web1/customer_form.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:

        cliente = Customer.objects.get(id=customer_id)
        

        check_permission(request, customer_id,Customer)

        form = CustomerForm(instance=cliente)
        context={"customer_id":customer_id, "form": form}
    return render(request, "web1/customer_form.html", context)

@login_required
def new_customer_form(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CustomerForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():

            cliente = form.save(commit=False)
            codigo = get_code("CUS")
            cliente.nombre_completo=form.cleaned_data["nombre"] + "_" + form.cleaned_data["apellido1"] + "_" + form.cleaned_data["apellido2"]
            cliente.code=codigo
            cliente.user = request.user
            cliente.save()


            # redirect to a new URL:
            return redirect("/web1/customer_list/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomerForm()
        context={"form": form,"nuevo_cliente":"si"}
    return render(request, "web1/customer_form.html", context)


def get_code(type_code):

    ultimo_registro = Serial_number.objects.get(type_code=type_code,year=2025)

    ultimo_numero = ultimo_registro.count
    nuevo_numero = str(ultimo_numero +1)
    s_ultimo_numero = nuevo_numero.zfill(5)
    codigo =  type_code + str(datetime.datetime.now().year)[2:] 
    codigo = codigo + s_ultimo_numero
    ultimo_registro.count=nuevo_numero
    ultimo_registro.save()

    return codigo

