import random
import time
import requests
import pandas as pd

def load_latest_report(sym):
    url = '	https://mops.twse.com.tw/mops/web/ajax_t164sb03'
    payload = {
        'encodeURIComponent': '1',
        'step': '2',
        'firstin': '1',
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'TYPEK': 'sii',
        'isnew': 'true',
        'co_id': str(sym),
    }
    time.sleep(random.uniform(1.5,5.4))
    res = requests.post(url, data=payload)
    return pd.read_html(res.text)


def read_stocks():
    with open('./stock.txt') as f:
        return list(filter(lambda x: x, [line.strip() for line in f.readlines()]))


def do_all():
    for stock in read_stocks():
        f = open("result.txt","a")
        df = load_latest_report(stock)[1]
        interested = {
            '股本合計': '股本合計',
            '流動資產合計': '流動資產合計',
            '負債總額': '負債總[計額]',
        }
        f.write(f"=== {stock} ===\n")
        for entry, regex in interested.items():
            f.write(f"{entry} => {df[df.iloc[:, 0].str.contains(regex)].iloc[0,1]}\n")
    f.close()
    print("Finish !")


if __name__ == '__main__':
    do_all()
