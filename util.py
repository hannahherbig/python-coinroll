import sys

def color(n, t=None, spec='+.8f'):
  return '\033[%dm%s\033[m' % (32 if n >= 0 else 31, format(t or n, spec))

def payout(x):
  return int(0.99 / float(x) * 65536)

def printf(s='', *args):
  sys.stdout.write('\r%s' % (s % args))
  sys.stdout.flush()

def puts(s='', *args):
  print(('\r%s' % (s % args)))
