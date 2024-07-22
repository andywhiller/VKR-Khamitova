from django.urls import path, include
from . import views

urlpatterns = [
    path('noteseditor/', views.NotesEditor.as_view(), name='notes_editor'),
    path('noteseditor/notes_editor_submit/', views.NotesEditor.as_view(), name='notes_editor1'),
    path('processor/<int:lesson>/<str:type>/', views.TestProcessor.as_view(), name='test_processor'),
    path('my/', views.UserTests.as_view(), name='my_tests'),
    path('add/', views.AddTestView.as_view(), name='add_test'),
    path('edit/<int:pk>/', views.EditTestView.as_view(), name='edit_test'),
    path('view/<int:pk>/', views.TestView.as_view(), name='view_test'),
    path('all_created/', views.AllCreatedTestsView.as_view(), name='all_created_tests'),
    path('question/delete/<int:pk>/', views.DeleteQuestion.as_view(), name='delete_question'),
    path('question/update/<int:pk>/', views.UpdateQuestion.as_view(), name='update_question'),
    path('checker/', views.TestChecker.as_view(), name='test_checker'),
    path('checker/<int:pk>/', views.TestCheckSaver.as_view(), name='test_check_saver'),
    path('notes/', views.NotesTest.as_view(), name='notes_test'),
    path('notes_readonly/<int:pk>/', views.NotesReadonlyView.as_view(), name='notes_readonly'),
    path('notes_lesson/<int:pk>/', views.NotesReadonlyLessonView.as_view(), name='notes_lesson'),
    path('variant/<int:pk>/', views.AddTestVariant.as_view(), name='test_variant'),
    path('variant/delete/', views.DeleteAnswerVariant.as_view(), name='test_variant_delete'),
]
