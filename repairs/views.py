from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Apartment, Room, Work, Material
from .forms import ApartmentForm, RoomForm, WorkForm, MaterialForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Apartment
from django.utils import timezone
from django.urls import reverse


def index(request):
    return render(request, 'repairs/index.html')


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


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')


@login_required
def apartment(request):
    # Получаем проекты текущего пользователя, сортируем по названию
    apartments = Apartment.objects.filter(user=request.user).order_by('name')
    print(f"Всего проектов для пользователя {request.user.username}: {apartments.count()}")  # Отладка
    if not apartments.exists():
        print("Нет проектов для этого пользователя. Добавьте проекты через админку или форму.")
    paginator = Paginator(apartments, 5)  # 5 проектов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(f"Объектов на странице {page_obj.number}: {page_obj.object_list.count()}")  # Отладка
    return render(request, 'repairs/apartment.html', {'page_obj': page_obj})


@login_required
def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    rooms = apartment.room_set.all()
    return render(request, 'repairs/apartment_detail.html', {'apartment': apartment, 'rooms': rooms})


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
            return redirect(reverse('apartment_detail', kwargs={'pk': pk}) + '#rooms')
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
            return redirect(reverse('apartment_detail', kwargs={'pk': apartment.id}) + '#rooms')
        else:
            return render(request, 'repairs/room_form.html',
                          {'form': form, 'apartment': apartment,
                           'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = RoomForm()
    return render(request, 'repairs/room_form.html', {'form': form, 'apartment': apartment})


@login_required
def room_edit(request, room_id):
    room = get_object_or_404(Room, pk=room_id, apartment__user=request.user)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комната успешно обновлена!')
            return redirect(reverse('apartment_detail', kwargs={'pk': room.apartment.id}) + '#rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'repairs/room_form.html', {'form': form, 'apartment': room.apartment})


@login_required
def room_delete(request, room_id):
    room = get_object_or_404(Room, pk=room_id, apartment__user=request.user)
    if request.method == 'POST':
        apartment_id = room.apartment.id
        room.delete()
        messages.success(request, 'Комната успешно удалена!')
        return redirect(reverse('apartment_detail', kwargs={'pk': apartment_id}) + '#rooms')
    return render(request, 'repairs/room_confirm_delete.html', {'room': room})


@login_required
def work_create(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.room = room
            # Если дата не указана, устанавливаем текущую дату
            if not work.date:
                work.date = timezone.now().date()
            work.save()
            return redirect(reverse('apartment_detail', kwargs={'pk': room.apartment.id}) + '#rooms')
    else:
        form = WorkForm(initial={'date': timezone.now().date()})  # Предустановка даты для GET
    return render(request, 'repairs/work_form.html', {
        'form': form,
        'room': room,
        'current_date': timezone.now().date(),
    })


@login_required
def work_edit(request, work_id):
    work = get_object_or_404(Work, pk=work_id, room__apartment__user=request.user)
    if request.method == 'POST':
        form = WorkForm(request.POST, instance=work)
        if form.is_valid():
            work = form.save(commit=False)
            if not form.cleaned_data['date']:  # Если дата не указана в форме
                work.date = timezone.now().date()
            work.save()
            for material in work.material_set.all():
                print(f"Material after edit: {material.name}, Cost: {material.cost}")
            return redirect(reverse('apartment_detail', kwargs={'pk': work.room.apartment.id}) + '#rooms')
        else:
            return render(request, 'repairs/work_form.html',
                          {'form': form, 'room': work.room, 'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        initial_data = {'date': work.date if work.date else timezone.now().date()}
        form = WorkForm(instance=work, initial=initial_data)
    return render(request, 'repairs/work_form.html', {
        'form': form,
        'room': work.room,
        'current_date': timezone.now().date(),
    })


@login_required
def work_delete(request, work_id):
    work = get_object_or_404(Work, pk=work_id, room__apartment__user=request.user)
    if request.method == 'POST':
        apartment_id = work.room.apartment.id
        work.delete()
        return redirect(reverse('apartment_detail', kwargs={'pk': apartment_id}) + '#rooms')
    return render(request, 'repairs/work_confirm_delete.html', {'work': work})


@login_required
def material_create(request, work_id):  # (12.09.25) material_create: Создаёт материал, привязывает его к комнате.
    work = get_object_or_404(Work, pk=work_id)
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.work = work
            material.save()
            return redirect(reverse('apartment_detail', kwargs={'pk': work.room.apartment.id}) + '#rooms')
        else:
            return render(request, 'repairs/material_form.html',
                          {'form': form, 'work': work, 'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = MaterialForm()
    return render(request, 'repairs/material_form.html', {'form': form, 'work': work})


@login_required
def material_edit(request, material_id):  # (12.09.25) material_edit: Редактирует существующий материал.
    material = get_object_or_404(Material, pk=material_id)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect(reverse('apartment_detail',
                                    kwargs={'pk': material.work.room.apartment.id}) + '#rooms')
        else:
            return render(request, 'repairs/material_form.html',
                          {'form': form, 'work': material.work,
                           'error': 'Пожалуйста, исправьте ошибки в форме'})
    else:
        form = MaterialForm(instance=material)
    return render(request, 'repairs/material_form.html', {'form': form, 'work': material.work})


@login_required
def material_delete(request, material_id):  # (12.09.25) material_delete: Удаляет материал с подтверждением.
    material = get_object_or_404(Material, pk=material_id)
    if request.method == 'POST':
        apartment_id = material.work.room.apartment.id
        material.delete()
        return redirect(reverse('apartment_detail', kwargs={'pk': apartment_id}) + '#rooms')
    return render(request, 'repairs/material_confirm_delete.html', {'material': material})


@login_required
def image_full(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk, user=request.user)
    return render(request, 'repairs/image_full.html', {'apartment': apartment})
