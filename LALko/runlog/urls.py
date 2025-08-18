from django.urls import path
from . import views

urlpatterns = [
    path("operations/", views.operation_list, name="operation_list"),
    path("operations/<int:pk>/", views.operation_detail, name="operation_detail"),
    path("my-operations/", views.my_operations, name="my_operations"),
    path("add-operation/", views.add_operation, name="add_operation"),
    path("machines/", views.machine_list, name="machine_list"),
]
