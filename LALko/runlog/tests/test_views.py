from django.test import TestCase
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from runlog.models import Machine, Operator, Task, Project, MachiningType, Operation

@pytest.mark.django_db
def test_operation_list_view(client):
    url = reverse("operation_list")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_operation_requires_login(client):
    url = reverse("add_operation")
    response = client.get(url)
    # pokud uživatel není přihlášený, měl by dostat redirect na login
    assert response.status_code == 302
    assert "/login" in response.url
