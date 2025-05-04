from django.urls import path
from . import views
from django.conf.urls import include

app_name = "web1"
urlpatterns = [
    path("", views.index2, name="index"),
    path("credentials/",views.check_credentials,name ="credentials"),
    path("customer_list/",views.customer_list,name="lista_clientes"),
    path("customer_list/<int:customer_id>",views.customer_form,name="formulario_cliente"),
    path("customer_list/new_customer",views.new_customer_form,name="formulario_nuevo_cliente"),
]

