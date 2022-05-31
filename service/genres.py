from typing import Dict, Any

from dao.genres import GenreDAO
from dao.model.genres import GenreSchema

genre_schema = GenreSchema()


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, genre_d):
        return genre_schema.dump(self.dao.create(genre_d))

    def update(self, rid, data: Dict[str, Any]):
        self.dao.update(rid, genre_schema.load(data))

    def delete(self, rid):
        self.dao.delete(rid)
