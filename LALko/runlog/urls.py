# runlog/urls.py
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/operations/', permanent=True)),
    path("operations/", views.operation_list, name="operation_list"),
    path("operations/<int:pk>/", views.operation_detail, name="operation_detail"),
    path("add-operation/", views.add_operation, name="add_operation"),
    #path("machines/", views.machine_list, name="machine_list"),
    path('operation/<int:pk>/edit/', views.edit_operation, name='edit_operation'),
    path('operation/<int:pk>/delete/', views.delete_operation, name='delete_operation'),
    
    # Tento řádek ponechejte, protože zajišťuje přesměrování
    path('my-operations/', RedirectView.as_view(url='/operations/', permanent=True), name='my_operations'),
    path('accounts/', include('django.contrib.auth.urls')),
]