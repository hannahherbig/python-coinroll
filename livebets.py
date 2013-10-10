import coinroll
from util import color

from decimal import Decimal
from collections import defaultdict

profits = defaultdict(Decimal)

seen = set()

print('user           | bet          | amount     | lucky < less  | diff        | profit')

try:
  while True:
    for bet in coinroll.livebets().data:
      if bet.id not in seen:
        seen.add(bet.id)
    
        profits[bet.user] += bet.diff

        print('%s | %s | %.8f | %s < %5d | %s | %s' % (bet.user, bet.id,
          bet.amount, color(bet.diff, bet.lucky, '5d'), bet.lessthan,
          color(bet.diff), color(profits[bet.user])))

except KeyboardInterrupt:
  pass
