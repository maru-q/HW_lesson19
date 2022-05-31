from typing import Dict, Any

from dao.director import DirectorDAO
from dao.model.director import DirectorSchema

director_schema = DirectorSchema()


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, director_d):
        return director_schema.dump(self.dao.create(director_d))

    def update(self, rid, data: Dict[str, Any]):
        self.dao.update(rid, director_schema.load(data))

    def delete(self, rid):
        self.dao.delete(rid)