from dao.model.user import User, UserSchema

user_schema = UserSchema()


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def get_by_username(self, username):
        return user_schema.dump(self.session.query(User).filter(User.username == username).first())

