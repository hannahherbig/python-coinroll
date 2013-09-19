import coinroll
import argparse
import sys

parser = argparse.ArgumentParser(description='Fetch the entire bet history of '
  'this user, and generate a data file that can be fed to gnuplot')
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('file')
args = parser.parse_args()

def color(n):
  return 32 if n >= 0 else 31

api = coinroll.Coinroll(args.user, args.password)
bets = float('inf')
offset = 0
profit = 0

with open(args.file, 'w') as f:
  while offset < bets:
    offset += 5

    if offset > bets:
      offset = bets

    r = api.bets(offset)
    bets = r.count

    for bet in reversed(r.bets):
      diff = bet.diff
      profit += diff

      f.write('%d %.8f\n' % (bet.num, profit))
      f.flush()

    sys.stdout.write('\r%d / %d = %.4f%%' % (offset, bets,
                                             offset * 100.0 / bets))
    sys.stdout.flush()

print
