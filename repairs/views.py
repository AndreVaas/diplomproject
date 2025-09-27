from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Apartment, Room, Work, Material
from .forms import ApartmentForm, RoomForm, WorkForm, MaterialForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib import messages


def signup_user(request):
    if request.method == "GET":
        return render(request, 'repairs/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('apartment')
            except IntegrityError:
                return render(request, 'repairs/signupuser.html', {
                    'form': UserCreationForm(),
                    'error': 'Пользователь с таким именем уже существует'
                })
        else:
            return render(request, 'repairs/signupuser.html', {
                'form': UserCreationForm(),
                'error': 'Пароли не совпадают'
            })


def login_user(request):
    if request.method == "GET":
        return render(request, 'repairs/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'repairs/loginuser.html', {
                'form': AuthenticationForm(),
                'error': 'Неверные имя пользователя или пароль'
            })
        else:
            login(request, user)
            return redirect('apartment')


@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')


@login_required
def apartment(request):
    apartments = Apartment.objects.filter(user=request.user)
    return render(request, 'repairs/apartment.html', {'apartments': apartments})


@login_required
def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk, user=request.user)
    rooms = apartment.room_set.all()
    return render(request, 'repairs/apartment_detail.html',
                  {'apartment': apartment, 'rooms': rooms})


@login_required
def apartment_create(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.user = request.user
            apartment.save()
            return redirect('apartment')
        else:
            return render(request, 'repairs/apartment_form.html',
                          {'form': form, 'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = ApartmentForm()
    return render(request, 'repairs/apartment_form.html', {'form': form})


@login_required
def apartment_update(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES, instance=apartment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект успешно обновлён!')
            return redirect('apartment_detail', pk=pk)
    else:
        form = ApartmentForm(instance=apartment)
    return render(request, 'repairs/apartment_form.html', {'form': form, 'apartment': apartment})


@login_required
def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk, user=request.user)
    if request.method == 'POST':
        apartment.delete()
        messages.success(request, 'Проект успешно удалён!')
        return redirect('apartment')
    return render(request, 'repairs/apartment_confirm_delete.html', {'apartment': apartment})


@login_required
def room_create(request, apartment_id):
    apartment = get_object_or_404(Apartment, pk=apartment_id, user=request.user)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.apartment = apartment
            room.save()
            return redirect('apartment_detail', pk=apartment.id)
        else:
            return render(request, 'repairs/room_form.html',
                          {'form': form, 'apartment': apartment,
                           'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = RoomForm()
    return render(request, 'repairs/room_form.html', {'form': form, 'apartment': apartment})


@login_required
def work_create(request, room_id):
    room = get_object_or_404(Room, pk=room_id, apartment__user=request.user)
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.room = room
            work.save()
            return redirect('apartment_detail', pk=room.apartment.id)
        else:
            return render(request, 'repairs/work_form.html',
                          {'form': form, 'room': room, 'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = WorkForm()
    return render(request, 'repairs/work_form.html', {'form': form, 'room': room})


@login_required
def work_edit(request, work_id):
    work = get_object_or_404(Work, pk=work_id, room__apartment__user=request.user)
    if request.method == 'POST':
        form = WorkForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect('apartment_detail', pk=work.room.apartment.id)
        else:
            return render(request, 'repairs/work_form.html',
                          {'form': form, 'room': work.room, 'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = WorkForm(instance=work)
    return render(request, 'repairs/work_form.html', {'form': form, 'room': work.room})


@login_required
def work_delete(request, work_id):
    work = get_object_or_404(Work, pk=work_id, room__apartment__user=request.user)
    if request.method == 'POST':
        apartment_id = work.room.apartment.id
        work.delete()
        return redirect('apartment_detail', pk=apartment_id)
    return render(request, 'repairs/work_confirm_delete.html', {'work': work})


@login_required
def material_create(request, room_id):  # (12.09.25) material_create: Создаёт материал, привязывает его к комнате.
    room = get_object_or_404(Room, pk=room_id, apartment__user=request.user)
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.room = room
            material.save()
            return redirect('apartment_detail', pk=room.apartment.id)
        else:
            return render(request, 'repairs/material_form.html',
                          {'form': form, 'room': room, 'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = MaterialForm()
    return render(request, 'repairs/material_form.html', {'form': form, 'room': room})


@login_required
def material_edit(request, material_id):  # (12.09.25) material_edit: Редактирует существующий материал.
    material = get_object_or_404(Material, pk=material_id, room__apartment__user=request.user)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('apartment_detail', pk=material.room.apartment.id)
        else:
            return render(request, 'repairs/material_form.html',
                          {'form': form, 'room': material.room,
                           'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = MaterialForm(instance=material)
    return render(request, 'repairs/material_form.html', {'form': form, 'room': material.room})


@login_required
def material_delete(request, material_id):  # (12.09.25) material_delete: Удаляет материал с подтверждением.
    material = get_object_or_404(Material, pk=material_id, room__apartment__user=request.user)
    if request.method == 'POST':
        apartment_id = material.room.apartment.id
        material.delete()
        return redirect('apartment_detail', pk=apartment_id)
    return render(request, 'repairs/material_confirm_delete.html', {'material': material})
