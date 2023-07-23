"""
_______________________________________
API layer for conversion of currencies.
ALso includes crypto currencies exchange
rates.
_______________________________________
"""

# Dependencies
import traceback
from flask import Flask
from requests import get
from dotenv import load_dotenv
from models.response import Response
from os import environ
from flask_cors import CORS, cross_origin
from random_utilities import log

from dotenv import load_dotenv

load_dotenv()

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
        conversion_response = get(
            f'https://api.fastforex.io/convert?from={_from_currency}&to={_to_currency}&amount={_from_amount}&api_key={environ["FASTFOREX_KEY"]}'
        )

        if conversion_response.status_code == 200:
            conversion = conversion_response.json()["result"]
            print(conversion)
            return Response(
                cd=200,
                dt=dict(
                    to_currency=_to_currency,
                    from_currency=_from_currency,
                    exchange_rate=conversion["rate"],
                    from_amount=from_amount,
                    to_amount=conversion[_to_currency],
                ),
            ).to_json()
        else:
            print("Error:", traceback.format_exc())
            return Response(cd=500, rs="Something went wrong.").to_json()
    except:
        log(traceback.format_exc())
        return Response(
            cd=400, rs="Something went wrong while accepting the conversion amount."
        ).to_json()


"""
_____________________________________
Gets a list of currencies available.
_____________________________________
"""


@hetch_translator.route("/translator/all", methods=["GET"])
@cross_origin()
def list_all_currencies():
    # normal and crypto currencies
    # n_currencies = get("https://openexchangerates.org/api/currencies.json")
    # c_currencies = get(
    #     "https://api.coingate.com/v2/currencies?native=true&enabled=true&kind=crypto"
    # )

    # format the crypto currency data
    # c_formatted = {}
    # for c_currency in c_currencies.json():
    #     c_formatted[c_currency["symbol"]] = c_currency["title"]

    # all = {**n_currencies.json(), **c_formatted}
    # print(all)
    # del dt["VEF"]

    all = dict(
        ZAR=dict(name="South African Rand", symbol="R"),
        USD=dict(name="United States Dollar", symbol="$"),
        CAD=dict(name="Canadian Dollar", symbol="C$"),
        AUD=dict(name="Australian Dollar", symbol="A$"),
        EUR=dict(name="European Euro", symbol="€"),
        JPY=dict(name="Japanese Yen", symbol="¥"),
        CHF=dict(name="Swiss Fanc", symbol="Fr."),
        CNY=dict(name="Chinese Yuan", symbol="¥"),
        SEK=dict(name="Swedish Krona", symbol="kr."),
        INR=dict(name="Indian Rupe", symbol="₹"),
        BTC=dict(name="Bitcoin", symbol="₿"),
        LTC=dict(name="Litecoin", symbol="Ł"),
        ETH=dict(name="Etherium", symbol="Ξ"),
        ADA=dict(name="Cardano", symbol="₳"),
    )

    return Response(cd=200, dt=all).to_json()
