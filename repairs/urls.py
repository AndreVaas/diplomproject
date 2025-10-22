from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('apartment/', views.apartment, name='apartment'),
    path('apartment/<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('apartment/new/', views.apartment_create, name='apartment_create'),
    path('signup/', views.signup_user, name='signupuser'),
    path('login/', views.login_user, name='loginuser'),
    path('logout/', views.logout_user, name='logoutuser'),
    path('apartment/<int:apartment_id>/room/new/', views.room_create, name='room_create'),
    path('room/<int:room_id>/work/new/', views.work_create, name='work_create'),
    path('room/<int:room_id>/edit/', views.room_edit, name='room_edit'),
    path('room/<int:room_id>/delete/', views.room_delete, name='room_delete'),
    path('work/<int:work_id>/edit/', views.work_edit, name='work_edit'),
    path('work/<int:work_id>/delete/', views.work_delete, name='work_delete'),
    path('material_create/<int:work_id>/', views.material_create, name='material_create'),
    path('material/<int:material_id>/edit/', views.material_edit, name='material_edit'),
    path('material/<int:material_id>/delete/', views.material_delete, name='material_delete'),
    path('<int:pk>/edit/', views.apartment_update, name='apartment_update'),
    path('<int:pk>/delete/', views.apartment_delete, name='apartment_delete'),
    path('apartment/<int:pk>/image/', views.image_full, name='image_full'),
]
