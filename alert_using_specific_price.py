import requests
from datetime import datetime
from time import sleep
from numerize import numerize
from win10toast import ToastNotifier

def crypto_rate(currency):
    api_server ='https://api.coingecko.com/api/v3/simple/price'
    payload ={'ids':currency,'vs_currencies':'usd','include_24hr_vol':'true','include_24hr_change':'true','include_last_updated_at':'true'}
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

def alert_up(asset,target):
    if (target-target*0.03) <= asset[1]['usd'] or asset[1]['usd'] >= target:
        toaster = ToastNotifier()
        toaster.show_toast('Price UP!',f"{asset[0].title()} is up {asset[1]['usd_24h_change']:.2f}% to ${float_to_str(asset[1]['usd'])}\n24h volume: ${numerize.numerize(asset[1]['usd_24h_vol'])}")
        return True
    return False

def alert_down(asset,target):
    if asset[1]['usd'] <= (target+target*0.03) or target >= asset[1]['usd']:
        toaster = ToastNotifier()
        toaster.show_toast('Price DOWN!',f"{asset[0].title()} is down {asset[1]['usd_24h_change']:.2f}% to ${float_to_str(asset[1]['usd'])}\n24h volume: ${numerize.numerize(asset[1]['usd_24h_vol'])}")
        return True
    return False

price_up={'kittenfinance':[50]}
price_down={'sator':[0.09]}

while True:
    ids=list(set(list(price_up.keys())+list(price_down.keys())))
    assets=crypto_rate(','.join(ids))
    for key in assets.keys():
        print(f"{key.title()} Price: ${assets[key]['usd']} 24h volume: ${numerize.numerize(assets[key]['usd_24h_vol'])} {datetime.utcfromtimestamp(assets[key]['last_updated_at']).strftime('%Y-%m-%d %H:%M:%S')}",end="\n")
    print('\n')
    for asset in assets.items():
        if asset[0] in price_up.keys() and price_up:
            for target in price_up[asset[0]]:
                if alert_up(asset,target):
                    price_up[asset[0]].remove(target)
                    break
            if not price_up[asset[0]]:
                del price_up[asset[0]]
                continue
        if asset[0] in price_down.keys() and price_down:
            for target in price_down[asset[0]]:
                if alert_down(asset,target):
                    price_down[asset[0]].remove(target)
                    break
            if not price_down[asset[0]]:
                del price_down[asset[0]]
                continue
    if not price_down and not price_up:
        break
    sleep(5)
