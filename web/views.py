from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.db.models import Q

from datetime import datetime

from .forms import UserForm, CompareForm, Orden
from .models import Car, Order

# Create your views here.
def index(request):
    return render(request, 'web/index.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('web:cars')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web:cars')
            else:
                return render(request, 'web/login.html', {'error_message': 'Your account has not been activated!'})
        else:
            return render(request, 'web/login.html', {'error_message': 'Invalid login'})
    return render(request, 'web/login.html')


def logout_user(request):
    logout(request)
    return redirect('web:index')


def register(request):
    if request.user.is_authenticated:
        return redirect('web:cars')
    uform = UserForm(request.POST or None)
    if uform.is_valid():
        user = uform.save(commit=False)
        username = uform.cleaned_data['username']
        password = uform.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web:dashboard')

    context = {
        "uform": uform,
    }

    return render(request, 'web/register.html', context)


def cars_page(request, pg=1):

    # Each page has 9 requests. That is fixed.
    start = (pg-1) * 9
    end = start + 9

    car_list = Car.objects.all()[start:end]
    context = {
        'cars': car_list
    }

    return render(request, 'web/cars.html', context)


def car_search(request):
    if request.method == 'GET':
        if request.GET.get('search'):
            search = request.GET.get('search')
        else:
            search = ''
        if request.GET.get('start'):
            start = int(request.GET.get('start'))
        else:
            start = 0
        if request.GET.get('end'):
            end = int(request.GET.get('end'))
        else:
            end = 9

        objs = Car.objects.filter(
            Q(marca__icontains=search) | Q(modelo__icontains=search)
        )[start:end]
        data = serializers.serialize('json', objs)
        return HttpResponse(data)


def cars(request):
    if request.method == 'GET':
        if request.GET.get('start'):
            start = int(request.GET.get('start'))
        else:
            start = 0
        if request.GET.get('end'):
            end = int(request.GET.get('end'))
        else:
            end = 9
            
        if request.GET.get('tipo'):
            tipo = request.GET.get('tipo')
            if tipo == 'all':
                tipo = ''
        else:
            tipo = ''

        if request.GET.get('cost_min'):
            cost_min = int(float(request.GET.get('cost_min')))
        else:
            cost_min = 0
        if request.GET.get('cost_max'):
            cost_max = int(float(request.GET.get('cost_max')))
        else:
            cost_max = 999999999
        if request.GET.get('combustible'):
            combustible = request.GET.getlist('combustible')
        else:
            combustible = ['Gasolina', 'Diesel']

        if len(combustible) > 1:
            objs = Car.objects.filter(
                Q(tipo__icontains=tipo) &
                Q(precio__gte=cost_min) &
                Q(precio__lte=cost_max) &
                (Q(combustible__icontains=combustible[0]) | Q(combustible__icontains=combustible[1]))
            )[start:end]

        else:
            objs = Car.objects.filter(
                tipo__icontains=tipo,
                precio__gte=cost_min,
                precio__lte=cost_max,
                combustible__icontains=combustible[0]
            )[start:end]

    else:
        objs = Car.objects.all()[:9]

    data = serializers.serialize('json', objs)
    return HttpResponse(data)


def car_details(request, cid):
    car = Car.objects.get(pk=cid)
    context = {
        'car': car,
        'form': Orden,
    }
    return render(request, 'web/car_details.html', context)


def order_car(request, cid):
    if not request.user.is_authenticated:
        return redirect('web:login')
    user = request.user
    car = Car.objects.get(pk=cid)

    if request.method == 'POST':
        try:
            address = request.POST['address']
            new = Order(
                user=user,
                car=car,
                amount=car.precio,
                address=address
            ).save()

            return HttpResponse("Your order has been placed!")
        except Exception as e:
            return HttpResponse("Uh Oh! Something's wrong! Report to the developer with the following error" +
                                e.__str__())
    return HttpResponseForbidden()

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('web:login')

    user = request.user
    orders = Order.objects.filter(user=user)

    context = {
        'orders': orders
    }

    return render(request, 'web/dashboard.html', context)


def compare(request):

    form = CompareForm(request.POST or None)
    if request.method == 'POST':
        car1 = int(request.POST['car1'])
        car2 = int(request.POST['car2'])

        car1 = Car.objects.get(pk=car1)
        car2 = Car.objects.get(pk=car2)

        data = {
            'car1_id': car1.id,
            'car1_name': car1.marca + " " + car1.modelo,
            'car1_foto': car1.foto.url,
            'car1_precio': car1.precio,
            'car1_anio':car1.anio,
            'car1_combustible':car1.combustible,
            'car1_puertas': car1.puertas,
            'car1_transmision': car1.transmision,
            'car1_motor': car1.motor,
            'car1_potencia': car1.potencia,
            'car1_tipo':car1.tipo,
            'car1_consumo': car1.consumo,
            'car1_estado':car1.estado,
            'car1_kilometros':car1.kilometros,
            'car1_pais':car1.pais,

            'car2_id': car2.id,
            'car2_name': car2.marca + " " + car2.modelo,
            'car2_foto': car2.foto.url,
            'car2_precio': car2.precio,
            'car2_anio':car2.anio,
            'car2_combustible':car2.combustible,
            'car2_puertas': car2.puertas,
            'car2_transmision': car2.transmision,
            'car2_motor': car2.motor,
            'car2_potencia': car2.potencia,
            'car2_tipo':car2.tipo,
            'car2_consumo': car2.consumo,
            'car2_estado':car2.estado,
            'car2_kilometros':car2.kilometros,
            'car2_pais':car2.pais,
        }

        html = '''
        <table class="table table-bordered" id="cmpTable">
            <tbody>
            <tr>
                <td>
                </td>
                <td>
                    <a href="car/{car1_id}">{car1_name}</a>
                </td>
                <td>
                    <a href="car/{car2_id}">{car2_name}</a>
                </td>
            </tr>
            <tr>
                <td class="w-25">
                </td>
                <td class="w-25 align-middle">
                    <img class="img-fluid" src="{car1_foto}" alt="">
                </td>
                <td class="w-25 align-middle">
                    <img class="img-fluid" src="{car2_foto}" alt="">
                </td>
            </tr>
            <tr>
                <td>
                    Precio ($)
                </td>
                <td>
                    {car1_precio}
                </td>
                <td>
                    {car2_precio}
                </td>
            </tr>
            <tr>
                <td>
                    Año
                </td>
                <td>
                    {car1_anio}
                </td>
                <td>
                    {car2_anio}
                </td>
            </tr>
            <tr>
                <td>
                    Tipo de combustible
                </td>
                <td>
                    {car1_combustible}
                </td>
                <td>
                    {car2_combustible}
                </td>
            </tr>
            <tr>
                <td>
                    Número de puertas
                </td>
                <td>
                    {car1_puertas}
                </td>
                <td>
                    {car2_puertas}
                </td>
            </tr>
            <tr>
                <td>
                    Tipo de transmisión
                </td>
                <td>
                    {car1_transmision}
                </td>
                <td>
                    {car2_transmision}
                </td>
            </tr>
            <tr>
                <td>
                    Motor (cc)
                </td>
                <td>
                    {car1_motor}
                </td>
                <td>
                    {car2_motor}
                </td>
            </tr>       
            <tr>
                <td>
                    Potencia máxima (PS)
                </td>
                <td>
                    {car1_potencia}
                </td>
                <td>
                    {car2_potencia}
                </td>
            </tr>
            <tr>
                <td>
                    Tipo de vehículo
                </td>
                <td>
                    {car1_tipo}
                </td>
                <td>
                    {car2_tipo}
                </td>
            </tr>
            <tr>
                <td>
                    Consumo
                </td>
                <td>
                    {car1_consumo}
                </td>
                <td>
                    {car2_consumo}
                </td>
            </tr>
            <tr>
                <td>
                    Estado
                </td>
                <td>
                    {car1_estado}
                </td>
                <td>
                    {car2_estado}
                </td>
            </tr>
            <tr>
                <td>
                    Kilometros
                </td>
                <td>
                    {car1_kilometros}
                </td>
                <td>
                    {car2_kilometros}
                </td>
            </tr>
            <tr>
                <td>
                    País
                </td>
                <td>
                    {car1_pais}
                </td>
                <td>
                    {car2_pais}
                </td>
            </tr>
            </tbody>
        </table>
        '''.format(**data)

        return HttpResponse(html)

    context = {
        'form': form
    }

    return render(request, 'web/compare.html', context)
