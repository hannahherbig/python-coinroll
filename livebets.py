import coinroll

from decimal import Decimal
from collections import defaultdict

def color(n):
  return 32 if n >= 0 else 31

profits = defaultdict(Decimal)

seen = set()

print 'user           | bet          | amount     | lucky < less  | diff        | profit'

while True:
  for bet in coinroll.livebets().data:
    if bet.id not in seen:
      seen.add(bet.id)
    
      profits[bet.user] += bet.diff

      print('%s | %s | %.8f | \033[%dm%5d\033[m < %5d | \033[%dm%+.8f\033[m | '
            '\033[%dm%+.8f\033[m' % (bet.user, bet.id, bet.amount,
              color(bet.diff), bet.lucky, bet.lessthan, color(bet.diff),
              bet.diff, color(profits[bet.user]), profits[bet.user]))
