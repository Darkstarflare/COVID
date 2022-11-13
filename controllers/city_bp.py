from flask import Blueprint
from flask_restful import Api, Resource

from models import database


CITY_BP = Blueprint('city', __name__, url_prefix='/city_api')
CITY_API = Api(CITY_BP)


class GetAllCities(Resource):

	def get(self):
		res = []
		for record in database.db.engine.execute('SELECT DISTINCT major_city FROM city_db'):
			res.append({'major_city': record.major_city})
		return res
			

class GetNameByZipCode(Resource):
	# Query handler
	def get(self, zipcode, city):
		data = {
			'from': 'GetNameByZipCode',
			'result': f'The major city in zipcode {zipcode} is {city}'
		}
		return data


CITY_API.add_resource(GetNameByZipCode, '/name_by_zipcode/<int:zipcode>/<string:city>')
CITY_API.add_resource(GetAllCities, '/all_cities/')