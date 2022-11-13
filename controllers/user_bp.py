from flask import Blueprint, request
from flask_restful import Api, Resource

USER_BP = Blueprint('user', __name__, url_prefix='/user_api')

USER_API = Api(USER_BP)

class GetAllUsers(Resource):

	def get(self):
		return 'All users'


class UserPassword(Resource):

	def get(self):
		# Get users' password
		data = request.get_json()
		user_name, password = data['user_name'], data['password']
		return f'user {user_name} password is {password}'

	def put(self):
		# Update users' password
		data = request.get_json()
		user_name, password = data['user_name'], data['password']
		return f'Updated user {user_name} password to {password}'



USER_API.add_resource(GetAllUsers, '/all_users')
USER_API.add_resource(UserPassword, '/user')