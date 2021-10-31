#!/usr/bin/python3
'''
we can have this utility script to add more currency informations
and to have additiional helper functions.
'''
import json
import logging

# log details and config
LOG_FILE = "./currency_converter.log"
logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s', filemode='w+', level=logging.INFO)
# previous exchange rate file
exchange_rate_file = "exchange_rate.json"
DEFAULT_CURRENCY = "EUR"
'''
SUPPORTED CURRENCY SYMBOLS for the forex_python library are:
['EUR', 'JPY', 'USD']
'''

CURRENCY_SYMBOL_MAP = {
    "€": "EUR",
    "eur": "EUR",
    "euro": "EUR",
    "¥": "JPY",
    "yen": "JPY",
    "jpy": "JPY",
    "usd": "USD",
    "$": "USD"
}

def write_to_file(converted_values, out_file):
    with open(out_file, "w+") as fp:
        for each in converted_values:
            json.dump(each, fp, indent=4)

def init_logger():
    logger=logging.getLogger()
    return logger