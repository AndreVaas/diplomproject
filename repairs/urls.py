from django.urls import path
from . import views

urlpatterns = [
    path('', views.apartment, name='apartment'),
    path('apartment/<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('apartment/new/', views.apartment_create, name='apartment_create'),
    path('signup/', views.signup_user, name='signupuser'),
    path('login/', views.login_user, name='loginuser'),
    path('logout/', views.logout_user, name='logoutuser'),
    path('apartment/<int:apartment_id>/room/new/', views.room_create, name='room_create'),
    path('room/<int:room_id>/work/new/', views.work_create, name='work_create'),
    path('work/<int:work_id>/edit/', views.work_edit, name='work_edit'),
    path('work/<int:work_id>/delete/', views.work_delete, name='work_delete'),
    path('room/<int:room_id>/material/new/', views.material_create, name='material_create'),
    path('material/<int:material_id>/edit/', views.material_edit, name='material_edit'),
    path('material/<int:material_id>/delete/', views.material_delete, name='material_delete'),
]
