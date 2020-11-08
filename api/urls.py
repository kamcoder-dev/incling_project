from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views
from rest_framework import routers
from .views import *


urlpatterns = [
    path('', apiOverview, name="api-overview"),
    path('auth', include('knox.urls')),
    path('auth/register', RegistrationAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('auth/user', UserAPI.as_view()),

    path('task/list', TaskListAPI, name='task-list'),
    path('task/create', TaskCreateAPI, name="task-create"),
    path('task/update/<str:pk>/', TaskUpdateAPI, name="task-update"),
    path('task/detail/<str:pk>/', TaskDetailAPI, name="task-detail"),
    path('task/delete/<str:pk>/', TaskDeleteAPI, name="task-delete"),

    path('tile/create', TileCreateAPI, name="tile-create"),
    path('tile/list', TileListAPI, name="tile-list"),
    path('tile/update/<str:pk>/', TileUpdateAPI, name="tile-update"),
    path('tile/detail/<str:pk>/', TileDetailAPI, name="tile-detail"),
    path('tile/delete/<str:pk>/', TileDeleteAPI, name="task-delete"),
]
