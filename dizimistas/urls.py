from django.urls import path
from .views import DizimistaListView

urlpatterns = [
    path('api/dizimistas/', DizimistaListView.as_view(), name='api-dizimistas'),
]
