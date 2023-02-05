# Crypto Prices Alert for Windows
Crypto prices alerts using CoinGecko API and ToastNotifier for Windows notifications.

## How To Use
Use alert_using_change_rate.py to get alert depending on the change rate of your targeted coin.

Modify the value of watchlist in the line 42 
(For example: watchlist='bitcoin,solana').

Modify the value of change_rate in line 43
(For example: change_rate=0.05 stand for a change rate of 5% up or down.)

Use alert_using_specific_price.py to get alert depending on the change rate of your targeted coin.

Modify the value of price_up in line 42
(For example : price_up={'bitcoin':[30000],'solana':[40]})

Modify the value of price_down in line 42
(For example : price_up={'bitcoin':[15000],'solana':[10]})


## Execution

Simply double click on the file after finishing with modification.

Ps: Make sure you have the necessary packages.
Use pip to install them.
