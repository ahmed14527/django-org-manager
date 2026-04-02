from django.urls import path
from .views import (
    CreateOrganizationView,
    AddUserToOrganizationView,
    ListOrganizationUsersView,
    SearchOrganizationUsersView
)

urlpatterns = [
    path('', CreateOrganizationView.as_view(), name='create-organization'),
    path('<uuid:organization_id>/users/', AddUserToOrganizationView.as_view(), name='add-user'),
    path('<uuid:organization_id>/users/list/', ListOrganizationUsersView.as_view(), name='list-users'),
    path('<uuid:organization_id>/users/search/', SearchOrganizationUsersView.as_view(), name='search-users'),
]