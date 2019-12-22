import csv
import csv2qif
import datetime

__mapping = {
    'date': 1,
    'price': 7,
    'recipient': 5,
    'desc': 6,
}


class dialect(csv.Dialect):
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


def row_converter(csv_row) -> csv2qif.Transaction:
    price = csv_row[__mapping['price']]
    if not price:
        price_income_index=__mapping['price']+1
        price = csv_row[price_income_index]

    return csv2qif.Transaction(
        date=datetime.datetime.strptime(csv_row[__mapping['date']], '%Y-%m-%d'),
        price=float(price),
        recipient=csv_row[__mapping['recipient']],
        desc=csv_row[__mapping['desc']]
    )
