import coinroll
import argparse
from fractions import Fraction

parser = argparse.ArgumentParser()
parser.add_argument('payout', type=float)
args = parser.parse_args()

lessthan = int(0.99 / args.payout * 65536)

game = coinroll.gameinfo(lessthan)

print('lessthan   : {:5d}'.format(game.lessthan))
print('min bet    : {:.8f}'.format(game.minbet))
print('max bet    : {:.8f}'.format(game.maxbet))
print('multiplier : {:f}'.format(game.multiplier))
print('odds       : {:f}'.format(game.odds))
print('house edge : {:f}'.format(game.houseedge))
