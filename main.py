#!/usr/bin/python3.10
# coding:utf-8
import random
import time
import requests
import pandas as pd
#第一季季報5/15前，第二季季報8/14前，第三季季報11/14前，年度財報次年3/31前。

def load_latest_report(sym):
    url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb03'
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
    with open("./stock.txt", mode="r", encoding="utf-8") as f:
        return list(filter(lambda x: x, [line.strip() for line in f.readlines()]))


def do_all():
    for stock in read_stocks():
        df = load_latest_report(stock)[1]
        capital_stock = {
            '股本合計': '股本合計',
        }
        for entry, regex in capital_stock.items():
            with open("capital_stock.txt", mode="a", encoding="utf-8") as f:
                f.write(f"{df[df.iloc[:, 0].str.contains(regex)].iloc[0,1]}\n")
        current_assets = {
            '流動資產合計': '流動資產合計',
        }
        for entry, regex in current_assets.items():
            with open("current_assets.txt", mode="a", encoding="utf-8") as f:
                f.write(f"{df[df.iloc[:, 0].str.contains(regex)].iloc[0,1]}\n")
        total_liabilities = {
            '負債總額': '負債總[計額]',
        }
        for entry, regex in total_liabilities.items():
            with open("total_liabilities.txt", mode="a", encoding="utf-8") as f:
                f.write(f"{df[df.iloc[:, 0].str.contains(regex)].iloc[0,1]}\n")
    print("Finish !")


if __name__ == '__main__':
    do_all()
