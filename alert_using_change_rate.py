import requests
from datetime import datetime
from time import sleep
from numerize import numerize
from win10toast import ToastNotifier

def crypto_rate(currency):
    api_server ='https://api.coingecko.com/api/v3/simple/price'
    payload ={'ids':currency,'vs_currencies':'usd','include_24hr_vol':'true','include_last_updated_at':'true'}
    response = requests.get(api_server,params=payload)
    result = response.json()
    return result

def float_to_str(f):
    float_string = repr(f)
    if 'e' in float_string:
        digits, exp = float_string.split('e')
        digits = digits.replace('.', '').replace('-', '')
        exp = int(exp)
        zero_padding = '0' * (abs(int(exp)) - 1)
        sign = '-' if f < 0 else ''
        if exp > 0:
            float_string = '{}{}{}.0'.format(sign, digits, zero_padding)
        else:
            float_string = '{}0.{}{}'.format(sign, zero_padding, digits)
    return float_string

def alert(asset):
    global watchlist_price
    dif=asset[1]['usd']-watchlist_price[asset[0]]
    target=watchlist_price[asset[0]]*change_rate
    if abs(dif) >= target:
        percentage='+'+'{:.2f}'.format((abs(dif)/watchlist_price[asset[0]])*100)+'%'
        watchlist_price[asset[0]]= asset[1]['usd']
        toaster=ToastNotifier()
        if dif >0:
            toaster.show_toast('Price UP!',f"{asset[0].title()} is up {percentage} to ${float_to_str(asset[1]['usd'])}\n24h volume: ${numerize.numerize(asset[1]['usd_24h_vol'])}")
        else:
            toaster.show_toast('Price DOWN!',f"{asset[0].title()} is down {percentage} to ${float_to_str(asset[1]['usd'])}\n24h volume: ${numerize.numerize(asset[1]['usd_24h_vol'])}")


watchlist='sator'
change_rate = 0.05
assets=crypto_rate(watchlist)
watchlist_price={}
for asset in assets.items():
    watchlist_price[asset[0]]=asset[1]['usd']


while True:
    assets=crypto_rate(watchlist)
    for key in assets.keys():
        print(f"{key.title()} Price: ${assets[key]['usd']} 24h volume: ${numerize.numerize(assets[key]['usd_24h_vol'])} {datetime.utcfromtimestamp(assets[key]['last_updated_at']).strftime('%Y-%m-%d %H:%M:%S')}",end="\n")
    print('\n')
    for asset in assets.items():
        alert(asset)
    sleep(5)

    
