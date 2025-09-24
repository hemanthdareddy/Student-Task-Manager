from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('subjects/', views.subjects_view, name='subjects'), 
    path('delete-subject/<int:subject_id>/', views.delete_subject_view, name='delete_subject'), 
    path('complete-task/<int:task_id>/', views.complete_task_view, name='complete_task'), 
    path('delete-task/<int:task_id>/', views.delete_task_view, name='delete_task'),  
    path('achievements/', views.achievements_view, name='achievements'),
]