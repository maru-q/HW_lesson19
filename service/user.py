from dao.user import UserDAO
from utils import get_hashed_password
from dao.model.user import UserSchema

user_schema = UserSchema()


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def register(self, data: dict):
        data["password"] = get_hashed_password(data["password"])
        return self.dao.create(data)

    def get_all(self):
        return user_schema.dump(self.dao.get_all(), many=True)

    def get_one(self, uid):
        return user_schema.dump(self.dao.get_by_id(uid))

    def update(self, uid, data):
        self.dao.update(uid, user_schema.load(data))
