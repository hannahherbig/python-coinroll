def color(n, t=None, spec='+.8f'):
  return '\033[{:d}m{}\033[m'.format(32 if n >= 0 else 31, format(t or n, spec))

def payout(x):
  return int(0.99 / float(x) * 65536)
