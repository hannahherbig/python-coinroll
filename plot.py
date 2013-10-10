import coinroll
import argparse
import sys

parser = argparse.ArgumentParser(description='Fetch the entire bet history of '
  'this user, and generate a data file that can be fed to gnuplot')
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('file')
args = parser.parse_args()

api = coinroll.Coinroll(args.user, args.password)
bets = float('inf')
offset = 0
profit = 0

try:
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

        f.write('{:d} {:.8f}\n'.format(bet.num, profit))
        f.flush()

      sys.stdout.write('\r{:d} / {:d} = {:.2%}'.format(offset, bets,
        offset / bets))
      sys.stdout.flush()

except KeyboardInterrupt:
  pass

finally:
  print()
