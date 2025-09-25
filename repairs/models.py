from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F, DecimalField


# Название проекта(Квартира, частный дом) (добавил 27.07.25)
class Apartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    total_area = models.FloatField()

    def __str__(self):
        return self.name

    # добавил методы модели Apartment,
    # total_cost и works_cost которые вычисляют общую стоимость ремонта для конкретного проекта
    # (добавил 04.09.25)
    # def total_cost(self):
    #     rooms = self.room_set.all()
    #     works_cost = sum(room.work_set.aggregate(total_cost=Sum('cost'))['total_cost'] or 0 for room in rooms)
    #     materials_cost = sum(
    #         room.material_set.aggregate(total_cost=Sum(F('cost') * F('quantity')))['total_cost'] or 0 for room in rooms)
    #     return works_cost + materials_cost

    def total_cost(self):
        return self.works_cost() + self.materials_cost()

    # Метод total_cost упрощён, используя works_cost и materials_cost. обновлено (12.09.25)
    def works_cost(self):
        rooms = self.room_set.all()
        return sum(room.work_set.aggregate(total_cost=Sum('cost'))['total_cost'] or 0 for room in rooms)

    def materials_cost(self):
        rooms = self.room_set.all()
        return sum(room.material_set.aggregate(total_cost=Sum(F('cost') * F('quantity'), output_field=DecimalField()))[
                       'total_cost'] or 0 for room in rooms)


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
    date = models.DateField()

    def __str__(self):
        return self.name


# Список материалов и подсчет нужного количества, подсчет квадратуры (добавил 02.08.25)
class Material(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)  # например: м², кг, л
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
