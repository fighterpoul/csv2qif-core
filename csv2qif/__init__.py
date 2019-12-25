import sys
import csv
import logging
import click
import importlib
import pkgutil
from csv2qif.core import Importer
from csv2qif import qif


logging.basicConfig(format='', level=logging.INFO)

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('csv2qif_')
}

__available_plugins = [plugin.replace('csv2qif_', '') for plugin in discovered_plugins.keys()]


@click.command()
@click.argument('csv_file', type=click.File('r'))
@click.argument('bank', type=click.Choice(__available_plugins, case_sensitive=True))
@click.argument('output', type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True))
@click.option('--account-name', '-a', required=False, type=str)
def main(csv_file, bank, account_name, output):
    reader = csv.reader(csv_file, dialect=discovered_plugins[bank].dialect)
    rows = [row for row in reader]
    importer = Importer(discovered_plugins[bank].row_converter)
    transactions = importer.map_transactions(rows)
    qif_entities = qif.map_transactions(transactions)
    qif.save(qif_entities, for_account=account_name, output=output)
    logging.info('{} entities properly exported to QIF file'.format(len(qif_entities)))
    return 0


@click.command()
def plugins():
    logging.info(', '.join(sorted(__available_plugins)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
