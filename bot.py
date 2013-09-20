import coinroll
import argparse
from decimal import Decimal

def payout(x):
  return int(0.99 / float(x) * 65536)

parser = argparse.ArgumentParser()
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('-s', '--start', type=Decimal, default=None)
parser.add_argument('-x', '--max', type=Decimal, default=Decimal('Infinity'))
parser.add_argument('-t', '--target', type=Decimal, default=Decimal('Infinity'))
parser.add_argument('-l', '--lessthan', type=int, default=payout(2))
parser.add_argument('-p', '--payout', type=payout, dest='lessthan',
                                      metavar='PAYOUT')
parser.add_argument('-a', '--add', action='store_true')
parser.add_argument('-i', '--interval', type=int, default=1)
parser.add_argument('-m', '--multiplier', type=int, default=2)

args = parser.parse_args()

def color(n):
  return 32 if n >= 0 else 31

bot = coinroll.Coinroll(args.user, args.password)
r = bot.stats()
game = coinroll.gameinfo(args.lessthan)
start = args.start or game.minbet
amount = start

loses = 0

print 'balance    | amount     | lucky < less  | diff        | profit'

try:
  while amount <= r.balance < args.target and amount <= args.max:
    r = bot.bet(args.lessthan, amount)

    print('%.8f | %.8f | \033[%dm%5d\033[m < %5d | \033[%dm%+.8f\033[m | '
          '\033[%dm%+.8f\033[m' % (r.balance, r.amount, color(r.diff), r.lucky,
            r.lessthan, color(r.diff), r.diff, color(r.profit), r.profit))

    if r.win:
      amount = start
      loses = 0

    else:
      loses += 1

      if loses % args.interval == 0:
        amount *= args.multiplier

        if args.add:
          amount += start

except KeyboardInterrupt:
  pass
