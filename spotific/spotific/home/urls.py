from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.registerPage, name='register_view'),
    path('register_error/', views.register_view, name='register_error_view'),
    path('Canciones/<str:id_cancion>/', views.canciones, name='canciones_view'),
    path('Artistas/<str:id_artista>/', views.artistas, name='artistas_view'),
    path('Albums/<str:id_album>/', views.albums, name='albums_view'),
    path('profile/', views.profile, name='profile_view'),
]