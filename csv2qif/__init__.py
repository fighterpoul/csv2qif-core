import sys
from collections import namedtuple
import csv
import logging
import click

Transaction = namedtuple('Transaction', ['date', 'price', 'recipient', 'desc'])

from csv2qif import banks
from csv2qif import qif


logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.argument('bank', type=click.Choice(banks.supported, case_sensitive=True))
@click.argument('output', type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True))
@click.option('--account-name', '-a', required=False, type=str)
def main(path, bank, account_name, output):
    with open(path, newline='') as f:
        reader = csv.reader(f, dialect=bank)
        rows = [row for row in reader]

    importer = banks.create_importer(bank)
    transactions = importer.map_transactions(rows)
    qif_entities = qif.map_transactions(transactions)
    qif.save(qif_entities, for_account=account_name, output=output)
    logging.info('{} entities properly exported to QIF file'.format(len(qif_entities)))


if __name__ == '__main__':
    sys.exit(main())
