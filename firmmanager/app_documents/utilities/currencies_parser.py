import re
from decimal import Decimal, getcontext

from bs4 import BeautifulSoup
import requests

from app_documents.models import Currency


class CurrenciesUpdater:

    def __init__(self):
        self.url = 'http://www.cbr.ru/scripts/XML_daily.asp'
        self.pattern = re.compile(r'\.val\("([^@]+@[^@]+\.[^@]+)"\);', re.MULTILINE | re.DOTALL)
        self.currencies = []

    def get_currencies(self):
        source = requests.get(self.url)
        bs_content = BeautifulSoup(source.content, 'lxml')
        currencies = bs_content.find_all(name='valute')
        for currency in currencies:
            currency = currency.encode()
            bs_currency = BeautifulSoup(currency, 'html.parser')
            title = bs_currency.find(name='name').contents[0]
            code = bs_currency.find(name='numcode').contents[0]
            char_code = bs_currency.find(name='charcode').contents[0]
            nominal = int(bs_currency.find(name='nominal').contents[0])
            cost = Decimal(bs_currency.find(name='value').contents[0].replace(',', '.'))
            self.currencies.append(
                {'title': title, 'code': code, 'char_code': char_code, 'nominal': nominal, 'cost': cost})

    def update_currencies(self):
        for currency in self.currencies:
            try:
                currency_object = Currency.objects.get(code=currency['code'])
            except Exception:
                currency_object = Currency(title=currency['title'],
                                           code=currency['code'],
                                           char_code=currency['char_code'],
                                           nominal=currency['nominal'],
                                           cost=currency['cost'])
                currency_object.save()


