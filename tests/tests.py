""" Implementation for tests files of the server """
import pytest
from server import convert_a_currency, list_all_currencies, hetch_translator
from flask.wrappers import Response
from json import loads
from random import randint

""" Testing conversion with a ZAR (South African Rand) currency from USD (American Dollar) """
def test_zar_currency_conversion():
	with hetch_translator.app_context():
		# r=response, d=data
		r = convert_a_currency("54.50", "zar")
		d = r.json
		assert type(r) is Response and r.status_code == 200 and type(d["data"]["to_amount"]) is float

""" Run tests with conversion to a EUR (Euro) from USD (US Dollar) """
def test_eur_currency_conversion():
	with hetch_translator.app_context():
		r = convert_a_currency("43.40", "eur")
		d = r.json
		result = d["data"]["to_amount"]
		assert type(r) is Response and r.status_code == 200 and type(result) is float


""" Test listing all currencies. """
def test_listing_currencies():
	with hetch_translator.app_context():
		r = list_all_currencies()
		r_data = r.json
		result = r_data.get("data")
		assert type(r) is Response and r.status_code == 200 and type(result) is not None and len(result.keys()) == 192


""" Run tests with a number of currencies possible """
def test_multiple_currency_conversion():
	with hetch_translator.app_context():
		r = list_all_currencies()
		r_data = r.json
		r_keys = r_data["data"].keys()
		start = randint(5, 10)
		random = randint(0, len(r_keys))

		if start + random < len(r_keys):
			end = (start + random)
		else:
			end = len(r_keys) - 1

		for index in range(random, end):
			currency_code = list(r_keys)[index]
			# c=conversion
			c = convert_a_currency("5.54", currency_code)
			if c.status_code == 200:
				if (index+1) == [random, end][-1]:
					assert True
			else:
				assert False
		
