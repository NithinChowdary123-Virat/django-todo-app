from django.urls import path
from . import views

urlpatterns = [
    path('',views.RegisterToDo.as_view(), name='register'),
    path("login/",views.LoginToDo.as_view(),name='login'),
    path("insert/",views.InsertToDo.as_view(),name = 'inserturl'),
    path('select/',views.SelectToDo.as_view(),name='selecturl'),
    path('update/<int:pk>',views.UpdateToDo.as_view(),name='updateurl'),
    path('delete/<int:pk>',views.DeleteToDo.as_view(),name='deleteurl'),
    path('logout/',views.LogoutToDo.as_view(), name='logout'),
               ]