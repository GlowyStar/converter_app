from django.urls import path
from .views import exchange
from .views import AsyncExchangeView

urlpatterns = [
    path('', exchange),
    path('api/v1/', AsyncExchangeView.as_view())
]
