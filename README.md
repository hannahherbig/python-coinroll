This is a simple wrapper around the [Coinroll](https://coinroll.it) API.
Well, coinroll.py is. The other files are examples of how you can use it.

bot.py is an example of the martingale strategy at 49.5% chance (2x payout).
It colors the numbers based on whether you won or lost, or if your profit is 
positive/negative. It starts at the lowest possible amount and doubles it each 
time it loses, and resets when it wins. If it tries to bet more than it has, it will also reset. It will stop once it breaks even or it's balance is less than the minimum bet.

history.py will fetch your entire bet history and present it similar to how
bot.py presents bet results.

plot.py will write your bet history to a file that can be parsed by gnuplot,
so you can get a pretty graph of your bet history.

You can run the scripts without any arguments for a usage message.

Please send tips to 1DvkfNva4LpTXJ7udThCQpQAuc9bu7V6XL
