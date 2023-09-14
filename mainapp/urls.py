from django.urls import path
from mainapp import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/',views.signin,name='signin'),
    path('Logout/',views.Logout,name='Logout'),
    path('settings/',views.settings,name='settings'),
    path('upload/',views.upload,name='upload'),
    path('likes/',views.likes,name="likes"),
    path('profiles/<str:pk>',views.profiles,name='profiles'),
    path('follows/',views.follows,name='follows'),
    path('search/',views.search, name='search'),
]
