# coding: utf-8

from oshlex.config import Rule, Configuration
from oshlex import handlers

# Defining rules
root = Rule('root')
server = Rule('server', unique=True, mandatory=True)
host = Rule('host', handler=handlers.text, unique=True, mandatory=True)
port = Rule('port', handler=handlers.integer, unique=True, mandatory=True)
user = Rule('user', unique=False, mandatory=False)
username = Rule('username', handler=handlers.text, unique=True, mandatory=True)
password = Rule('password', handler=handlers.text, unique=True, mandatory=True)

# Chaining rules together
user.add(username)
user.add(password)
server.add(host)
server.add(port)
server.add(user)
root.add(server)

conf = Configuration(root)
conf.read('./example.conf')
