"""
_______________________________________
API layer for conversion of currencies.
ALso includes crypto currencies exchange
rates.
_______________________________________
"""

# Dependencies
import traceback
import freecurrencyapi
from flask import Flask
from requests import get
from dotenv import load_dotenv
from models.response import Response
from os import environ
from flask_cors import CORS, cross_origin
from random_utilities import log

from dotenv import load_dotenv

load_dotenv()

currency_client = freecurrencyapi.Client(environ.get("CURRENCY_API_KEY"))

hetch_translator = Flask(__name__)
CORS(hetch_translator, resources={r"*": {"origins": "*"}})

"""
_____________________________________
Convert a currency with USD as the base.
_____________________________________
"""


@hetch_translator.route(
    "/translator/translate/<_from_amount>/<_from_currency>/<_to_currency>",
    methods=["GET"],
)
@cross_origin()
def convert_a_currency(_from_amount: str, _from_currency: str, _to_currency: str):
    try:
        from_amount = float(_from_amount)

        if from_amount == 0:
            from_amount = 1

        latest_conversions = currency_client.latest(_from_currency)

        if latest_conversions["data"].get(_from_currency):
            return Response(
                cd=200,
                dt=dict(
                    to_currency=_to_currency,
                    from_currency=_from_currency,
                    exchange_rate=latest_conversions["data"][_to_currency],
                    from_amount=_from_amount,
                    to_amount=0
                    if _from_amount == "0"
                    else latest_conversions["data"][_from_currency] * from_amount,
                ),
            ).to_json()
        else:
            log(traceback.format_exc())
            return Response(cd=500, rs="Something went wrong.").to_json()
    except:
        log(traceback.format_exc())
        return Response(
            cd=400,
            rs="Something went wrong while accepting the conversion amount or currency code.",
        ).to_json()


"""
_____________________________________
Gets a list of currencies available.
_____________________________________
"""


@hetch_translator.route("/translator/all", methods=["GET"])
@cross_origin()
def list_all_currencies():
    all = {
        "ZAR": {
            "code": "ZAR",
            "name": "South African Rand",
            "name_plural": "South African rand",
            "symbol": "R",
        },
        "EUR": {"code": "EUR", "name": "Euro", "name_plural": "Euros", "symbol": "€"},
        "USD": {
            "code": "USD",
            "name": "US Dollar",
            "name_plural": "US dollars",
            "symbol": "$",
        },
        "JPY": {
            "code": "JPY",
            "name": "Japanese Yen",
            "name_plural": "Japanese yen",
            "symbol": "￥",
        },
        "BGN": {
            "code": "BGN",
            "name": "Bulgarian Lev",
            "name_plural": "Bulgarian leva",
            "symbol": "лв.",
        },
        "CZK": {
            "code": "CZK",
            "name": "Czech Republic Koruna",
            "name_plural": "Czech Republic korunas",
            "symbol": "Kč",
        },
        "DKK": {
            "code": "DKK",
            "name": "Danish Krone",
            "name_plural": "Danish kroner",
            "symbol": "kr",
        },
        "GBP": {
            "code": "GBP",
            "name": "British Pound Sterling",
            "name_plural": "British pounds sterling",
            "symbol": "£",
        },
        "HUF": {
            "code": "HUF",
            "name": "Hungarian Forint",
            "name_plural": "Hungarian forints",
            "symbol": "Ft",
        },
        "PLN": {
            "code": "PLN",
            "name": "Polish Zloty",
            "name_plural": "Polish zlotys",
            "symbol": "zł",
        },
        "RON": {
            "code": "RON",
            "name": "Romanian Leu",
            "name_plural": "Romanian lei",
            "symbol": "RON",
        },
        "SEK": {
            "code": "SEK",
            "name": "Swedish Krona",
            "name_plural": "Swedish kronor",
            "symbol": "kr",
        },
        "CHF": {
            "code": "CHF",
            "name": "Swiss Franc",
            "name_plural": "Swiss francs",
            "symbol": "CHF",
        },
        "ISK": {
            "code": "ISK",
            "name": "Icelandic Króna",
            "name_plural": "Icelandic krónur",
            "symbol": "kr",
        },
        "NOK": {
            "code": "NOK",
            "name": "Norwegian Krone",
            "name_plural": "Norwegian kroner",
            "symbol": "kr",
        },
        "HRK": {
            "code": "HRK",
            "name": "Croatian Kuna",
            "name_plural": "Croatian kunas",
            "symbol": "kn",
        },
        "RUB": {
            "code": "RUB",
            "name": "Russian Ruble",
            "name_plural": "Russian rubles",
            "symbol": "py6.",
        },
        "TRY": {
            "code": "TRY",
            "name": "Turkish Lira",
            "name_plural": "Turkish Lira",
            "symbol": "TL",
        },
        "AUD": {
            "code": "AUD",
            "name": "Australian Dollar",
            "name_plural": "Australian dollars",
            "symbol": "$",
        },
        "BRL": {
            "code": "BRL",
            "name": "Brazilian Real",
            "name_plural": "Brazilian reals",
            "symbol": "R$",
        },
        "CAD": {
            "code": "CAD",
            "name": "Canadian Dollar",
            "name_plural": "Canadian dollars",
            "symbol": "$",
        },
        "CNY": {
            "code": "CNY",
            "name": "Chinese Yuan",
            "name_plural": "Chinese yuan",
            "symbol": "CN¥",
        },
        "HKD": {
            "code": "HKD",
            "name": "Hong Kong Dollar",
            "name_plural": "Hong Kong dollars",
            "symbol": "$",
        },
        "IDR": {
            "code": "IDR",
            "name": "Indonesian Rupiah",
            "name_plural": "Indonesian rupiahs",
            "symbol": "Rp",
        },
        "ILS": {
            "code": "ILS",
            "name": "Israeli New Sheqel",
            "name_plural": "Israeli new sheqels",
            "symbol": "₪",
        },
        "INR": {
            "code": "INR",
            "name": "Indian Rupee",
            "name_plural": "Indian rupees",
            "symbol": "টকা",
        },
        "KRW": {
            "code": "KRW",
            "name": "South Korean Won",
            "name_plural": "South Korean won",
            "symbol": "₩",
        },
        "MXN": {
            "code": "MXN",
            "name": "Mexican Peso",
            "name_plural": "Mexican pesos",
            "symbol": "$",
        },
        "MYR": {
            "code": "MYR",
            "name": "Malaysian Ringgit",
            "name_plural": "Malaysian ringgits",
            "symbol": "RM",
        },
        "NZD": {
            "code": "NZD",
            "name": "New Zealand Dollar",
            "name_plural": "New Zealand dollars",
            "symbol": "$",
        },
        "PHP": {
            "code": "PHP",
            "name": "Philippine Peso",
            "name_plural": "Philippine pesos",
            "symbol": "₱",
        },
        "SGD": {
            "code": "SGD",
            "name": "Singapore Dollar",
            "name_plural": "Singapore dollars",
            "symbol": "$",
        },
        "THB": {
            "code": "THB",
            "name": "Thai Baht",
            "name_plural": "Thai baht",
            "symbol": "฿",
        },
    }

    return Response(cd=200, dt=all).to_json()
