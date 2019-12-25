import csv
from collections import namedtuple

Transaction = namedtuple('Transaction', ['date', 'price', 'recipient', 'desc'])


class Importer(object):

    def __init__(self, row_converter):
        self.row_converter = row_converter

    def map_transactions(self, csv_rows):
        data = csv_rows[1:]
        return [self.row_converter(row) for row in data if len(row) > 2]