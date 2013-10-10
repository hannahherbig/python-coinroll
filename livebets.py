import coinroll
from util import color

from decimal import Decimal
from collections import defaultdict

profits = defaultdict(Decimal)

seen = set()

print('user           | bet          | amount     | lucky < less  | '
      'diff        | profit')

try:
  while True:
    for bet in coinroll.livebets().data:
      if bet.id not in seen:
        seen.add(bet.id)
    
        profits[bet.user] += bet.diff

        print('{} | {} | {:.8f} | {} < {:5d} | {} | {}'.format(bet.user, bet.id,
          bet.amount, color(bet.diff, bet.lucky, '5d'), bet.lessthan,
          color(bet.diff), color(profits[bet.user])))

except KeyboardInterrupt:
  pass
