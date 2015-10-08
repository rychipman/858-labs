from zoodb import *
from debug import *

import hashlib
import random

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    cred_db = cred_setup()
    cred = cred_db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == password:
        return newtoken(cred_db, cred)
    else:
        return None

def register(username, password):
    person_db = person_setup()
    person = person_db.query(Person).get(username)
    if person:
        return None
    cred_db = cred_setup()
    newperson = Person()
    newperson.username = username
    person_db.add(newperson)
    person_db.commit()
    newcred = Cred()
    newcred.username = username
    newcred.password = password
    cred_db.add(newcred)
    cred_db.commit()
    return newtoken(cred_db, newcred)

def check_token(username, token):
    cred_db = cred_setup()
    cred = cred_db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

