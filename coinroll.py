# Wrapper for coinroll.it's API

import requests
from urllib import parse
from decimal import Decimal
from collections import namedtuple

BASE_URI = 'https://coinroll.it'
ONE_SATOSHI = Decimal('0.00000001')
ONE_BTC = 100000000

# convert a number in satoshis to BTC
def btc(x):
  return ONE_SATOSHI * x

# convert a number in BTC to satoshis if it's not already an integer
def sats(x):
  if not isinstance(x, int):
    x = int(x * ONE_BTC)
  return x

# the request method throws this when the 'result' is 0 (error)
class RequestException(Exception):
  pass

# a bunch of namedtuples used below

BetResult = namedtuple('BetResult', 'id lessthan amount lucky nonce win diff '
                                    'balance date profit bets wins')

Game = namedtuple('Game', 'lessthan minbet maxbet multiplier odds houseedge')

Stats = namedtuple('Stats', 'balance profit bets wins')

Withdraw = namedtuple('Withdraw', 'deferred amount txid balance')

DepositStatus = namedtuple('DepositStatus', 'confirmed withdrawal amount')

BetQueryResult = namedtuple('BetQueryResult', 'id user lessthan amount lucky '
                                              'multiplier nonce win delta '
                                              'timestamp txid released secret '
                                              'secretHash')

Bets = namedtuple('Bets', 'bets count')

Bet = namedtuple('Bet', 'id num lessthan amount lucky multiplier nonce win '
                        'diff display timestamp when date')

LiveBets = namedtuple('LiveBets', 'bets volume data')

LiveBet = namedtuple('LiveBet', 'user id amount lessthan lucky win multiplier '
                                'display timestamp diff')

Leader = namedtuple('Leader', 'user bets profit volume active')

# helper method
def request(path, **params):
  res = requests.post(parse.urljoin(BASE_URI, path), data=params)
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
    r = self.request('bet', lessthan=lessthan, amount=sats(amount))

    return BetResult(r['id'], r['lessthan'], btc(r['amount']), r['lucky'],
                     r['nonce'], r['win'], btc(r['diff']), btc(r['balance']),
                     r['date'], btc(r['profit']), r['bets'], r['wins'])

  def stats(self):
    r = self.request('getbalance')

    return Stats(btc(r['balance']), btc(r['profit']), r['bets'], r['wins'])

  def withdraw(self, address, amount):
    r = self.request('withdraw', address=address, amount=sats(amount))

    return Withdraw(r['deferred'], btc(r['amount']), r['txid'],
                    btc(r['balance']))

  def depositstatus(self):
    r = self.request('depositstatus')

    return DepositStatus(r['confirmed'], r['deferred'], btc(r['amount']))

  def bets(self, offset):
    r = self.request('getbets', offset=offset)

    bets = []

    for b in r['bets']:
      bets.append(Bet(b['id'], b['num'], b['lessthan'], btc(b['amount']),
                      b['lucky'], b['multiplier'], b['nonce'], b['win'],
                      btc(b['diff']), b['display'], b['timestamp'], b['when'],
                      b['date']))

    return Bets(bets, r['count'])

# Since these methods don't require authentication, they are outside of the
# Coinroll class.

def querybet(id):
  r = request('querybet', id=id)

  return BetQueryResult(r['id'], r['user'], r['lessthan'], btc(r['amount']),
                        r['lucky'], r['multiplier'], r['nonce'], r['win'],
                        btc(r['delta']), r['timestamp'], r['txid'],
                        r['released'], r['secret'], r['secrethash'])

def gameinfo(lessthan):
  r = request('getgameinfo', lessthan=lessthan)

  return Game(r['lessthan'], btc(r['minbet']), btc(r['maxbet']),
              r['multiplier'], r['odds'], r['houseedge'])

# these ones don't seem to be documented

def livebets():
  r = request('livebets')

  data = []

  for b in r['data']:
    diff = b['display'] - b['amount'] if b['win'] else b['display']
    data.append(LiveBet(b['user'], b['id'], btc(b['amount']), b['lessthan'],
                        b['lucky'], b['win'], b['multiplier'],
                        btc(b['display']), b['timestamp'], btc(diff)))

  return LiveBets(r['bets'].replace(',', ''),
                  Decimal(r['volume'].replace(',', '')), data)

def leaderboard():
  r = request('leaderboard')

  leaders = []

  for user, bets, profit, volume, active in r['data']:
    leaders.append(Leader(user, bets, btc(profit), btc(volume), active))

  return leaders
