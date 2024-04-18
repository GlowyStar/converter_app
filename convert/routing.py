from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from exchange_app.views import AsyncExchangeView

application = ProtocolTypeRouter({
    "http": URLRouter([
        path('api/v1/', AsyncExchangeView.as_asgi()),
    ]),
})
