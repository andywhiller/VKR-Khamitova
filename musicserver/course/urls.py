from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.MyCoursesView.as_view(), name='my_courses'),
    path('<int:pk>/', views.CourseView.as_view(), name='current_course'),
    path('signup/<int:pk>/', views.CourseSignUpView.as_view(), name='course_sign_up'),
    path('signout/<int:pk>/', views.CourseSignOutView.as_view(), name='course_sign_out'),
    path('add/', views.AddCourseView.as_view(), name='add_course'),
    path('delete/<int:pk>/', views.DeleteCourseView.as_view(), name='delete_course'),
    path('update/<int:pk>/', views.UpdateCourseView.as_view(), name='update_course'),
    path('rating/<int:pk>/', views.CourseRatingView.as_view(), name='course_rating'),
    path('rate/<int:pk>/', views.RateCourseView.as_view(), name='rate_course'),
]
