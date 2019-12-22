import csv
from . import ing, millennium

supported = ['millennium', 'ing']

csv.register_dialect('ing', ing.dialect)
csv.register_dialect('millennium', millennium.dialect)


class Importer(object):

    def __init__(self, row_converter):
        self.row_converter = row_converter

    def map_transactions(self, csv_rows):
        data = csv_rows[1:]
        return [self.row_converter(row) for row in data if len(row) > 2]


def create_importer(bank) -> Importer:
    if bank not in supported:
        raise KeyError('{} is unsupported name of bank. Only {} are supported.'.format(type, supported))

    result = {
        'millennium': millennium.row_converter,
        'ing': ing.row_converter,
    }[bank]

    return Importer(result)
