"""
_______________________________________
API layer for conversion of currencies.
ALso includes crypto currencies exchange
rates.
_______________________________________
"""

# Dependencies
from flask import Flask
from requests import get
from dotenv import load_dotenv
from models.response import Response
from os import environ

from dotenv import load_dotenv
load_dotenv()

hetch_translator = Flask(__name__)


"""
_____________________________________
Convert a currency with USD as the base.
_____________________________________
"""


@hetch_translator.route("/hetch-translator/convert/<from_amount>/<to_currency>", methods=["GET"])
def convert_a_currency(from_amount: str, to_currency: str) -> str:
    try:
        from_amount = float(from_amount)
    except:
        return Response(cd=400, rs="Invalid conversion amount provided.").to_json()
    to_currency = to_currency.upper()

    r_currencies = get("https://openexchangerates.org/api/currencies.json")
    if r_currencies.status_code:
        currencies = r_currencies.json()
        currency_keys = currencies.keys()

        r_ex_rate = get(
            f'https://api.coingate.com/v2/rates/merchant/USD/{to_currency}')
        try:
            exchange_rate = float(r_ex_rate.text)
        except:
            oex_rates_r = get(f'https://openexchangerates.org/api/latest.json?app_id={environ["OE_KEY"]}')
            if oex_rates_r.status_code == 200:
                oex_data = oex_rates_r.json()
                oex_keys = oex_data["rates"].keys()
                if to_currency in oex_keys:
                    exchange_rate = oex_data["rates"][to_currency]
                else:
                    return Response(cd=400, rs="Unsupported currency.").to_json()
            else:
                return Response(cd=500, rs="Something went wrong.").to_json()
                
        r_data = dict(
            to_currency=to_currency, from_currency="USD",
            exchange_rate=exchange_rate, from_amount=from_amount,
            to_amount=(from_amount * exchange_rate)
        )

        return Response(cd=200, dt=r_data).to_json()
    else:
        return Response(cd=500, rs="Something went wrong.").to_json()


"""
_____________________________________
Gets a list of currencies available.
_____________________________________
"""


@hetch_translator.route("/hetch-translator/", methods=["GET"])
def list_all_currencies():
    # normal and crypto currencies
    n_currencies = get("https://openexchangerates.org/api/currencies.json")
    c_currencies = get(
        "https://api.coingate.com/v2/currencies?native=true&enabled=true&kind=crypto")

    # format the crypto currency data
    c_formatted = {}
    for c_currency in c_currencies.json():
        c_formatted[c_currency["symbol"]] = c_currency["title"]

    dt = {**n_currencies.json(), **c_formatted}
    del dt["VEF"]
    return Response(cd=200, dt=dt).to_json()
