from django.urls import path
from .views import ConfiguracaoIgrejaView, UserProfileView, ChangePasswordView

urlpatterns = [
    path('api/configuracao/igreja/', ConfiguracaoIgrejaView.as_view(), name='api-config-igreja'),
    path('api/configuracao/tema/', UserProfileView.as_view(), name='api-config-tema'),
    path('api/auth/change-password/', ChangePasswordView.as_view(), name='api-change-password'),
]
