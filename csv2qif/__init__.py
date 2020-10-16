import sys
import csv
import logging
import click
import importlib
import pkgutil
from csv2qif.core import Importer
from csv2qif import qif


logging.basicConfig(format='', level=logging.INFO)

__discovered_plugins = {
    name.replace('csv2qif_', ''): importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('csv2qif_')
}

__available_plugins = [plugin.replace('csv2qif_', '') for plugin in __discovered_plugins.keys()]


def __check_encoding(csv_file):
    from chardet.universaldetector import UniversalDetector
    with open(csv_file, 'rb') as file:
        detector = UniversalDetector()
        for line in file.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        if 'encoding' in detector.result and detector.result['encoding']:
            return detector.result['encoding']
        else:
            raise UnicodeError('Failed to check encoding of the file {}'.format(csv_file))


@click.command()
@click.argument('csv_file', type=click.Path(exists=True))
@click.argument('bank', type=click.Choice(__available_plugins, case_sensitive=True))
@click.argument('output_qif_file', type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True))
@click.option('--account-name', '-a', required=False, type=str)
def main(csv_file, bank, account_name, output_qif_file):
    with open(csv_file, encoding=__check_encoding(csv_file)) as csv_file:
        reader = csv.reader(csv_file, dialect=__discovered_plugins[bank].dialect)
        rows = [row for row in reader]
    importer = Importer(row_converter=__discovered_plugins[bank].row_converter,
                        row_filter=__discovered_plugins[bank].row_filter if 'row_filter' in dir(__discovered_plugins[bank]) else None)
    transactions = importer.map_transactions(rows)
    qif_entities = qif.map_transactions(transactions)
    qif.save(qif_entities, for_account=account_name, output=output_qif_file)
    logging.info('{} entities properly exported to QIF file'.format(len(qif_entities)))
    return 0


@click.command()
def plugins():
    logging.info(', '.join(sorted(__available_plugins)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
