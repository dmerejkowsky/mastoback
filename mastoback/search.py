import whoosh.index
import whoosh.fields
import whoosh.qparser

schema = whoosh.fields.Schema(
    title=whoosh.fields.TEXT(stored=True),
    path=whoosh.fields.ID(stored=True),
    content=whoosh.fields.TEXT
)

index = whoosh.index.create_in("indexdir", schema)

writer = index.writer()
writer.add_document(
    title="First document",
    path="/a",
    content="This is the first document"
)

writer.add_document(
    title="Second document",
    path="/b",
    content="This is the second document"
)

writer.commit()

index = whoosh.index.open_dir("indexdir")
writer = index.writer()
writer.add_document(
    title="First doc bis",
    path="/c",
    content="there's more than one first",
)
writer.commit()

with index.searcher() as searcher:
    query = whoosh.qparser.QueryParser("content", index.schema).parse("first")
    results = searcher.search(query)
    for result in results:
        print(result)
