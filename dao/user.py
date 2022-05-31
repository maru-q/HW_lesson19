from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def create(self, data: dict):

        new_user = User(**data)
        self.session.add(new_user)
        self.session.commit()
        return ""

    def get_all(self):
        return self.session.query(User).all()

    def get_by_id(self, uid):
        return self.session.query(User).get(uid)

    def update(self, uid, data):
        self.session.query(User).filter(User.id == uid).update(data)
        self.session.commit()
