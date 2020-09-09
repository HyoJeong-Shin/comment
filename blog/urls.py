from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('comment/update/<int:pk>',views.comment_update, name='comment_update'),
    path('comment/delete/<int:pk>',views.comment_delete, name='comment_delete'),
]