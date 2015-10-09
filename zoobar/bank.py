from zoodb import *
from debug import *

import time

def transfer(sender, recipient, zoobars):
    bank_db = bank_setup()
    sender_bank = bank_db.query(Bank).get(sender)
    recipient_bank = bank_db.query(Bank).get(recipient)

    sender_balance = sender_bank.zoobars - zoobars
    recipient_balance = recipient_bank.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    sender_bank.zoobars = sender_balance
    recipient_bank.zoobars = recipient_balance
    bank_db.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    db = bank_setup()
    bank = db.query(Bank).get(username)
    return bank.zoobars

def register(username):
    bank_db = bank_setup()
    newbank = Bank()
    newbank.username = username
    newbank.zoobars = 10
    bank_db.add(newbank)
    bank_db.commit()

def get_log(username):
    db = transfer_setup()
    return db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))

