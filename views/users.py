from flask import request
from flask_restx import Resource, Namespace

from implemented import user_service
from utils import auth_required, admin_required

user_ns = Namespace("users")


@user_ns.route("/")
class UsersView(Resource):

    @auth_required
    @admin_required
    def get(self):
        return user_service.get_all(), 200

    def post(self):
        user_service.register(request.json)
        return {}, 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    @admin_required
    def get(self, uid):
        return user_service.get_one(uid), 200

    @auth_required
    def put(self, uid):
        user_service.update(uid, request.json)
        return "", 204
