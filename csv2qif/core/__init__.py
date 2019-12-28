from collections import namedtuple

Transaction = namedtuple('Transaction', ['date', 'price', 'recipient', 'desc'])


class Importer(object):

    def __init__(self, row_converter, row_filter=None):
        self.row_converter = row_converter
        self.row_filter = row_filter if row_filter else lambda row: len(row) > 2

    def map_transactions(self, csv_rows):
        converted = [self.row_converter(row) for row in csv_rows if self.row_filter(row)]
        return [row for row in converted if row]
