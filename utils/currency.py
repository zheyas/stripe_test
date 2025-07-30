import xml.etree.ElementTree as ET
from decimal import Decimal

import requests


def get_exchange_rate(from_currency: str, to_currency: str) -> Decimal:
    # Поддерживаем только обмен в рубли
    if to_currency.lower() != 'rub':
        raise ValueError("This function supports only conversion to RUB")

    if from_currency.lower() == 'rub':
        return Decimal('1')

    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    response.raise_for_status()

    tree = ET.fromstring(response.content)
    for valute in tree.findall('Valute'):
        char_code = valute.find('CharCode').text
        if char_code.lower() == from_currency.lower():
            value = valute.find('Value').text
            nominal = valute.find('Nominal').text
            # В ЦБ курс за nominal единиц валюты
            rate = Decimal(value.replace(',', '.')) / Decimal(nominal)
            return rate

    raise Exception(f"Currency {from_currency} not found in CBR data")
