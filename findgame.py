import coinroll
import argparse
from fractions import Fraction

parser = argparse.ArgumentParser()
parser.add_argument('payout', type=float)
args = parser.parse_args()

lessthan = int(0.99 / args.payout * 65536)

game = coinroll.gameinfo(lessthan)

print('lessthan   : %5d' % game.lessthan)
print('min bet    : %.8f' % game.minbet)
print('max bet    : %.8f' % game.maxbet)
print('multiplier : %f' % game.multiplier)
print('odds       : %f' % game.odds)
print('house edge : %f' % game.houseedge)
