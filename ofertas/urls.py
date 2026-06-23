from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfertaViewSet

router = DefaultRouter()
router.register('ofertas', OfertaViewSet, basename='ofertas')

urlpatterns = [
    path('api/', include(router.urls)),
]
