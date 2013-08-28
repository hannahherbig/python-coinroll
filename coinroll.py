# Wrapper for coinroll.it's API

import requests
import urlparse

BASE_URI = 'https://coinroll.it'

# the request method throws this when the 'result' is 0 (error)
class RequestException(Exception):
  pass

# helper method
def request(path, **params):
  res = requests.post(urlparse.urljoin(BASE_URI, path), data=params)
  data = res.json()
  if data['result']:
    return data
  else:
    raise RequestException('error on %s: %s' % (path, data['result']))

class Coinroll(object):
  def __init__(self, user, password):
    self.user = user
    self.password = password

  # helper method
  def request(self, path, **params):
    return request(path, user=self.user, password=self.password, **params)

  # Everything from here is just wrappers around the API.
  # Read https://coinroll.it/api to see how to use them. 

  def deposit(self):
    return self.request('deposit')

  def bet(self, lessthan, amount):
    return self.request('bet', lessthan=lessthan, amount=amount)

  def stats(self):
    return self.request('getbalance')

  def withdraw(self, address, amount):
    return self.request('withdraw', address=address, amount=amount)

  def depositstatus(self):
    return self.request('depositstatus')

  def bets(self, offset):
    return self.request('getbets', offset=offset)

# Since these methods don't require authentication, they are outside of the
# Coinroll class.

def querybet(id):
  return request('querybet', id=id)

def gameinfo(lessthan):
  return request('getgameinfo', lessthan=lessthan)
