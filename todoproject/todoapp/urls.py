from django.urls import path
from .import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('delete/<int:todo_id>/', views.delete, name='delete'),
    path('done/<int:todo_id>/', views.mark_as_done, name='done')
]
