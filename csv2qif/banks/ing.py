import csv
import csv2qif
import datetime

__mapping = {
    'date': 0,
    'price': 8,
    'recipient': 2,
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
    price = str(csv_row[__mapping['price']])
    if not price:
        blocked_index = 10
        price = str(csv_row[blocked_index])
    return csv2qif.Transaction(
        date=datetime.datetime.strptime(csv_row[__mapping['date']], '%Y-%m-%d'),
        price=float(price.replace(',', '.')),
        recipient=csv_row[__mapping['recipient']],
        desc=csv_row[__mapping['desc']]
    )
