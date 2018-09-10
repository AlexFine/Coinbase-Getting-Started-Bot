# Coinbase-Getting-Started-Bot
This is a simple bot to make trades on the Coinbase API. It's easy to understand, and provides an easy way to get started.
# Description
If the market jumps by a predetermined amount in a short amount of time, open a buy position for 4 minutes then sell (the average total time of large price jumps)
# Features
- Buy if:
  - 1.0025% in 10s
  - 1.0040% in 30s
  - 1.0070% in 55s
- Tests post only and taker orders, you can customize which you choose 
- Buys and sells at best current price 
  - Tries a buy order at the current price, if it's rejected, place the buy order for 1¢ lower than asking 
