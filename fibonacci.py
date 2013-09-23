import coinroll
import argparse
from decimal import Decimal

def color(n):
  return 32 if n >= 0 else 31

parser = argparse.ArgumentParser()
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('-b', '--base', type=Decimal, default=None)
parser.add_argument('-x', '--max', type=Decimal, default=Decimal('Infinity'))
parser.add_argument('-t', '--target', type=Decimal, default=Decimal('Infinity'))
parser.add_argument('-s', '--sequence', type=int, nargs='*', default=[1, 2])

args = parser.parse_args()

lessthan = 32440

bot = coinroll.Coinroll(args.user, args.password)
r = bot.stats()
game = coinroll.gameinfo(lessthan)
base = args.base or game.minbet
seq = args.sequence
index = 0

print 'balance    | amount     | lucky < less  | diff        | profit'

try:
  while True:
    amount = seq[index] * base
    
    if r.balance < amount or r.balance >= args.target or args.max < amount:
      break
    
    r = bot.bet(lessthan, amount)

    print('%.8f | %.8f | \033[%dm%5d\033[m < %5d | \033[%dm%+.8f\033[m | '
          '\033[%dm%+.8f\033[m' % (r.balance, r.amount, color(r.diff), r.lucky,
            r.lessthan, color(r.diff), r.diff, color(r.profit), r.profit))

    if r.win:
      index -= 2

      if index < 0:
        index = 0

    else:
      index += 1
      
      if len(seq) <= index:
        seq.append(seq[-2] + seq[-1])

except KeyboardInterrupt:
  pass
