import coinroll
from util import color
import argparse

parser = argparse.ArgumentParser(description='Fetch the entire bet history of '
  'this user, and output it to the terminal')
parser.add_argument('user')
parser.add_argument('password')
args = parser.parse_args()

api = coinroll.Coinroll(args.user, args.password)
bets = float('inf')
offset = 0
profit = 0

print('number | amount     | lucky < less  | diff        | profit')

try:
  while offset < bets:
    offset += 5

    if offset > bets:
      offset = bets

    r = api.bets(offset)
    bets = r.count

    for bet in reversed(r.bets):
      diff = bet.diff
      profit += diff

      print('{:6d} | {:.8f} | {} < {:5d} | {} | {}'.format(bet.num, bet.amount,
        color(diff, bet.lucky, '5d'), bet.lessthan, color(diff), color(profit)))

except KeyboardInterrupt:
  pass
