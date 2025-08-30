from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Přesměrování z kořenové adresy na seznam operací
    path('', RedirectView.as_view(url='/operations/', permanent=True)),
    
    # URL cesty pro operace
    path("operations/filter/", views.operation_filter, name="operation_filter"),
    path("operations/results/", views.operation_results, name="operation_results"),
    path("activity_log/", views.activity_log, name="activity_log"),
    path("operations/", views.operation_list, name="operation_list"),
    path("operations/<int:pk>/", views.operation_detail, name="operation_detail"),
    path('operation/add/', views.manage_operation, name='add_operation'),
    path('operation/edit/<int:pk>/', views.manage_operation, name='edit_operation'),
    path('operations/<int:pk>/delete/', views.delete_operation, name='delete_operation'),
    
    # Všechny URL pro přihlášení, odhlášení atd.
    path('accounts/', include('django.contrib.auth.urls')),
]