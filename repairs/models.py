from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F, DecimalField
from django.utils import timezone


# Название проекта(Квартира, частный дом) (добавил 27.07.25)
class Apartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    total_area = models.FloatField()
    image = models.ImageField(upload_to='apartment_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def total_cost(self):
        return self.works_cost() + self.materials_cost()

    def works_cost(self):
        rooms = self.room_set.all()
        return sum(room.work_set.aggregate(total_cost=Sum('cost'))['total_cost'] or 0 for room in rooms)

    def materials_cost(self):
        rooms = self.room_set.all()
        total_materials_cost = 0
        for room in rooms:
            for work in room.work_set.all():
                materials_cost = work.material_set.aggregate(
                    total_cost=Sum(F('cost') * F('quantity'), output_field=DecimalField())
                )['total_cost'] or 0
                total_materials_cost += materials_cost
        return total_materials_cost


# Разбивка по комнатам(кухня, ванна, и тд) (добавил 02.08.25)
class Room(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    area = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.apartment.name})"


# Виды работ (добавил 02.08.25)
class Work(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.name


# Список материалов и подсчет нужного количества, подсчет квадратуры (добавил 02.08.25)
class Material(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='material_set', null=True, blank=True )
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
