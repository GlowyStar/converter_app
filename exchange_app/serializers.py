from rest_framework import serializers
import aiohttp
import asyncio

CURRENCIES = None

async def get_currencies():
    global CURRENCIES
    if CURRENCIES is None:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.exchangerate-api.com/v4/latest/USD') as resp:
                response = await resp.json()
        CURRENCIES = response.get('rates')
    return CURRENCIES

class ExchangeSerializer(serializers.Serializer):
    from_amount = serializers.FloatField(help_text="Amount of money to convert")
    from_curr = serializers.ChoiceField(choices=[], help_text="Currency of the money to convert")
    to_curr = serializers.ChoiceField(choices=[], help_text="Currency to convert the money to")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currencies = asyncio.run(get_currencies())
        self.fields['from_curr'].choices = [(curr, curr) for curr in currencies]
        self.fields['to_curr'].choices = [(curr, curr) for curr in currencies]
