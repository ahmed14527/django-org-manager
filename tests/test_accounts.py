import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='test@example.com',
        full_name='Test User',
        password='testpass123'
    )
    return user

@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'full_name': 'New User',
        'password': 'TestPass123!'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert 'access_token' in response.data

@pytest.mark.django_db
def test_user_login(api_client, test_user):
    url = reverse('login')
    data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert 'access_token' in response.data

@pytest.mark.django_db
def test_user_login_invalid(api_client):
    url = reverse('login')
    data = {
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    }
    response = api_client.post(url, data)
    assert response.status_code == 401