import click
from path import Path
import mastoback.client
import mastoback.store
import mastoback.search


@click.command()
@click.option('--drop', is_flag=True)
def fetch(drop: bool = False) -> None:
    mastodon = mastoback.client.login()
    account = mastodon.account_verify_credentials()
    print("Logged in as", account.username)
    store = mastoback.store.Store()
    if drop:
        store.drop()

    latest_id = store.get_latest_id()
    index_path = Path("index")
    index = mastoback.search.Index(index_path, drop=drop)
    i = 0
    for status in mastoback.client.yield_statuses(mastodon, account.id, since_id=latest_id, limit=200):
        toot = mastoback.toot_from_status(status)
        store.add_toot(toot)
        index.add_toot(toot)
        i += 1
    if i:
        print("Stored", i, "new toots")
    else:
        print("No new toots")
    index.commit()


@click.command()
@click.argument("query")
def search(query: str) -> None:
    store = mastoback.store.Store()
    index = mastoback.search.Index()
    print("Looking for", query, "in index")
    for toot_id in index.search_text(query):
        toot = store.get_by_id(toot_id)
        print(toot.text)


@click.group()
def cli() -> None:
    pass


cli.add_command(search)
cli.add_command(fetch)
