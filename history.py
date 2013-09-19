import coinroll
import argparse

parser = argparse.ArgumentParser(description='Fetch the entire bet history of '
  'this user, and output it to the terminal')
parser.add_argument('user')
parser.add_argument('password')
args = parser.parse_args()

def color(n):
  return 32 if n >= 0 else 31

api = coinroll.Coinroll(args.user, args.password)
bets = float('inf')
offset = 0
profit = 0

print 'every number is in satoshis except for lucky and less'
print 'amount   | lucky < less  | diff      | profit'

while offset < bets:
  offset += 5

  if offset > bets:
    offset = bets

  r = api.bets(offset)
  bets = r.count

  for bet in reversed(r.bets):
    diff = bet.diff
    profit += diff

    print('%.8f | \033[%dm%5d\033[m < %5d | \033[%dm%+.8f\033[m | '
          '\033[%dm%+.8f\033[m' % (bet.amount, color(diff), bet.lucky,
            bet.lessthan, color(diff), diff, color(profit), profit))
