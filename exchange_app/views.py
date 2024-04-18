from django.shortcuts import render
import requests
from asgiref.sync import async_to_sync
import aiohttp
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExchangeSerializer

def exchange(request):
    response = requests.get(url='https://api.exchangerate-api.com/v4/latest/USD').json()
    currencies = response.get('rates')

    if request.method == 'GET':
        context = {
            'currencies': currencies
        }

        return render(request=request, template_name='exchange_app/index.html', context=context)

    if request.method == 'POST':
        from_amount = float(request.POST.get('from-amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((currencies[to_curr] / currencies[from_curr]) * float(from_amount), 2)

        context = {
            'from_curr': from_curr,
            'to_curr': to_curr,
            'from_amount': from_amount,
            'currencies': currencies,
            'converted_amount': converted_amount
        }

        return render(request=request, template_name='exchange_app/index.html', context=context)


class AsyncExchangeView(APIView):
    serializer_class = ExchangeSerializer

    def get(self, request):
        currencies = async_to_sync(self.get_currencies)()
        return Response({'currencies': currencies})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            from_amount = serializer.validated_data['from_amount']
            from_curr = serializer.validated_data['from_curr']
            to_curr = serializer.validated_data['to_curr']
            currencies = async_to_sync(self.get_currencies)()
            converted_amount = round((currencies[to_curr] / currencies[from_curr]) * float(from_amount), 2)
            return Response({'converted_amount': converted_amount})
        else:
            return Response(serializer.errors, status=400)

    async def get_currencies(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.exchangerate-api.com/v4/latest/USD') as resp:
                response = await resp.json()
        return response.get('rates')

