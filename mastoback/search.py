from path import Path
from typing import Generator

import whoosh.index
import whoosh.fields
import whoosh.qparser

from mastoback import Toot


class Index():
    def __init__(self, index_path: Path, drop: bool = False) -> None:

        schema = whoosh.fields.Schema(
            id=whoosh.fields.ID(stored=True),
            text=whoosh.fields.TEXT
        )

        if drop:
            index_path.rmtree_p()
            index_path.mkdir()
        else:
            index_path.mkdir_p()

        index_exists = whoosh.index.exists_in(index_path)
        if index_exists:
            self.index = whoosh.index.open_dir(index_path)
        else:
            self.index = whoosh.index.create_in(index_path, schema)
        self.writer = self.index.writer()

    def add_toot(self, toot: Toot) -> None:
        self.writer.add_document(id=toot.id, text=toot.text)

    def commit(self) -> None:
        self.writer.commit()

    def search_text(self, query: str) -> Generator[int, None, None]:
        with self.index.searcher() as searcher:
            query = whoosh.qparser.QueryParser("text", self.index.schema).parse(query)
            results = searcher.search(query)
            for result in results:
                yield result.id
