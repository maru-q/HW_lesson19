from typing import Dict, Any

from dao.model.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Director).get(bid)

    def get_all(self):
        return self.session.query(Director).all()

    def create(self, director_d):
        ent = Director(**director_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        director = self.get_one(rid)
        self.session.delete(director)
        self.session.commit()

    def update(self, rid: int, data: Dict[str, Any]):
        self.session.query(Director).filter(Director.id == rid).update(data)
        self.session.commit()
