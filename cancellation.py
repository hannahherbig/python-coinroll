import coinroll
from util import color
import argparse
from decimal import Decimal

parser = argparse.ArgumentParser()
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('sequence', type=int, nargs='+')
parser.add_argument('-b', '--base', type=Decimal, default=None)
parser.add_argument('-x', '--max', type=Decimal, default=Decimal('Infinity'))

args = parser.parse_args()

lessthan = 32440

bot = coinroll.Coinroll(args.user, args.password)
r = bot.stats()
game = coinroll.gameinfo(lessthan)
base = args.base or game.minbet
seq = args.sequence

print('balance    | amount     | lucky < less  | diff        | profit')

try:
  while len(seq) > 0:
    size = seq[0]
    
    if len(seq) > 1:
      size += seq[-1]
    
    amount = size * base
    
    if r.balance <= amount or args.max < amount:
      break
    
    r = bot.bet(lessthan, amount)

    print('%.8f | %.8f | %s < %5d | %s | %s' % (r.balance, r.amount,
      color(r.diff, r.lucky, '5d'), r.lessthan, color(r.diff), color(r.profit)))

    if r.win:
      seq.pop(0)
      
      if len(seq) > 0:
        seq.pop()

    else:
      seq.append(size)

except KeyboardInterrupt:
  pass
