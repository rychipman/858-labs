from debug import *
from zoodb import *
import rpclib

def transfer(sender, recipient, zoobars):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('transfer', sender=sender, recipient=recipient, zoobars=zoobars)
        return ret

def balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('balance', username=username)
        return ret

def register(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('register', username=username)
        return ret
