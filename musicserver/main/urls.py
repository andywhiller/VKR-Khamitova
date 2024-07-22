from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='mainindex'),
    path('courses/', include('course.urls')),
    path('lessons/', include('lessons.urls')),
    path('tests/', include('tests.urls')),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('openindex/', views.OpenIndexView.as_view(), name='openindex'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('commonindex/', views.CommonIndexView.as_view(), name='commonindex'),
    path('info/', views.info, name='info'),
    path('settings/', views.settings, name='settings'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('profile/edit/<int:pk>/', views.EditUserProfileView.as_view(), name='edit_profile'),
]
