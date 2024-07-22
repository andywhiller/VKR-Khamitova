from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:pk>/', views.AddLessonView.as_view(), name='add_lesson'),
    path('view/<int:pk>/', views.LessonView.as_view(), name='view_lesson'),
    path('update/<int:pk>/', views.UpdateLessonView.as_view(), name='update_lesson'),
    path('delete/<int:pk>/', views.DeleteLessonView.as_view(), name='delete_lesson'),
]
