import requests
from django.db.transaction import atomic

from app_documents.models import Currency


class CurrenciesUpdater:

    def __init__(self):
        self.url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        self.currencies = []

    def get_currencies(self):
        source = requests.get(self.url)
        json_source = source.json()
        self.currencies.append(json_source['Valute']['USD'])
        self.currencies.append(json_source['Valute']['EUR'])

    @atomic
    def update_currencies(self):
        for currency in self.currencies:
            try:
                currency_object = Currency.objects.get(code=currency['NumCode'])
                currency_object.cost = currency['Value']
                currency_object.save()
            except Exception:
                Currency.objects.create(title=currency['Name'],
                                        code=currency['NumCode'],
                                        char_code=currency['CharCode'],
                                        nominal=currency['Nominal'],
                                        cost=currency['Value'])


