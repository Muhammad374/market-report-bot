import requests

def get_usdt():
    url = "https://api.nobitex.ir/market/stats"
    
    data = {
        "srcCurrency": "usdt",
        "dstCurrency": "rls"
    }

    r = requests.post(url, json=data).json()

    price = r["stats"]["usdt-rls"]["latest"]

    return int(price) // 10   # تبدیل ریال به تومان


print(get_usdt())
