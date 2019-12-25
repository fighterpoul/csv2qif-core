from datetime import datetime
from csv2qif.core import Transaction
import os


class QifEntity(object):

    def __init__(self, date: datetime, price: float, recipient='', desc='', category=''):
        self.date = date
        self.price = price
        self.recipient = recipient
        self.desc = desc
        self.category = category

    @property
    def qif_node(self):
        return {
            'D': self.date.strftime('%m/%d/%Y'),
            'T': self.price,
            'C': 'c',
            'P': self.recipient,
            'M': self.desc,
            'L': self.category,
        }

    @property
    def node_separator(self):
        return '^{}'.format(os.linesep)


class AccountEntity(object):

    def __init__(self, name):
        self.name = name

    @property
    def qif_node(self):
        return {
            '!': 'Account',
            'N': self.name if self.name else '',
            'T': 'Bank',
            '^': '',
            '!Type:': 'Bank'
        }

    @property
    def node_separator(self):
        return ''


def map_transactions(transactions):
    return [__map_transaction(t) for t in transactions]


def __map_transaction(transaction: Transaction):
    return QifEntity(
        date=transaction.date,
        price=transaction.price,
        recipient=transaction.recipient,
        desc=transaction.desc
    )


def __create_qif_content(qif_entities, for_account) -> str:
    qif_representables = [AccountEntity(name=for_account)] + qif_entities
    result = ''
    for qif_rep in qif_representables:
        for key, value in qif_rep.qif_node.items():
            result += '{}{}{}'.format(key, value, os.linesep)
        result += qif_rep.node_separator
    return result


def save(qif_entities, for_account, output):
    content = __create_qif_content(qif_entities, for_account)
    with open(output, "w") as qif_file:
        qif_file.write(content)
