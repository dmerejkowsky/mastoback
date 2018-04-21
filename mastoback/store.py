from typing import Any

from mastoback import Toot

import pymongo


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

    def get_by_id(self, id: int) -> Any:
        return self.collection.find_one({"id": id})

    def add_toot(self, toot: Toot) -> None:
        self.collection.insert({
            "id": toot.id,
            "status": toot.status,
            "text": toot.text
        })
