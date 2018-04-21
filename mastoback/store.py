from typing import Any, Dict, Generator, NewType
from mastoback import Toot

import pymongo

Doc = NewType('Doc', Dict[str, Any])


def toot_from_doc(doc: Doc) -> Toot:
    return Toot(
        doc["id"],
        doc["text"],
        doc["url"],
        doc["status"],
    )


class Store():
    def __init__(self) -> None:
        client = pymongo.MongoClient()
        db = client.mastoback
        self.collection = db.toots

    def get_latest_id(self) -> int:
        latest = self.collection.find_one(
            sort=[("id", -1)]
        )
        if not latest:
            return 0
        latest_id: int = latest["id"]
        return latest_id

    def drop(self) -> None:
        self.collection.drop()

    def get_by_id(self, id: int) -> Toot:
        doc = self.collection.find_one({"id": id})
        return toot_from_doc(doc)

    def get_latest_toots(self, num: int) -> Generator[Toot, None, None]:
        docs = (
            self.collection
                .find()
                .sort([('id', pymongo.DESCENDING)])
                .limit(num)
        )
        for doc in docs:
            yield toot_from_doc(doc)

    def add_toot(self, toot: Toot) -> None:
        self.collection.insert({
            "id": toot.id,
            "status": toot.status,
            "text": toot.text,
            "url": toot.url,
        })
