from django.urls import path
from .views import CreateItemView, ListItemsView

urlpatterns = [
    path('<uuid:organization_id>/', CreateItemView.as_view(), name='create-item'),
    path('<uuid:organization_id>/list/', ListItemsView.as_view(), name='list-items'),
]