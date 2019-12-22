import csv
import csv2qif
import datetime
import re

__price_regex = re.compile('[a-zA-Z ]')
__text_regex = re.compile('[\t ]+')

__mapping = {
    'date': 0,
    'price': 4,
    'recipient': 1,
    'desc': 3,
}


class dialect(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


def row_converter(csv_row) -> csv2qif.Transaction:
    price = csv_row[__mapping['price']]
    price = __price_regex.sub('', price)
    price = price.replace(',', '.')

    return csv2qif.Transaction(
        date=datetime.datetime.strptime(csv_row[__mapping['date']], '%Y-%m-%d'),
        price=float(price),
        recipient=__text_regex.sub(' ', csv_row[__mapping['recipient']]),
        desc=__text_regex.sub(' ', csv_row[__mapping['desc']])
    )
