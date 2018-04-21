import sys

import click
from path import Path

from mastoback import Toot
import mastoback.client
import mastoback.store
import mastoback.search
import mastoback.config


def get_index_path() -> Path:
    config = mastoback.config.read_config()
    from_conf = config["index_path"]
    return Path(from_conf)


def open_index(drop: bool = False) -> mastoback.search.Index:
    index_path = get_index_path()
    return mastoback.search.Index(index_path, drop=drop)


@click.command()
@click.option('--drop', is_flag=True)
def fetch(drop: bool = False) -> None:
    mastodon = mastoback.client.login()
    account = mastodon.account_verify_credentials()
    print("Logged in as", account.username)
    store = mastoback.store.Store()
    if drop:
        store.drop()

    index = open_index(drop=drop)
    latest_id = store.get_latest_id()
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
    index = open_index(drop=False)
    ids = list(index.search_text(query))
    if not ids:
        sys.exit("No toot found matching query")
    print("Found", len(ids), "results")
    for toot_id in ids:
        toot = store.get_by_id(toot_id)
        print_toot(toot)


@click.command()
@click.argument("n", type=int)
def latest(n: int) -> None:
    store = mastoback.store.Store()
    toots = store.get_latest_toots(num=n)
    for toot in toots:
        print_toot(toot)


def print_toot(toot: Toot) -> None:
    print("-" * 80)
    print(toot.text.strip())
    print(toot.url)
    print()


@click.group()
def cli() -> None:
    pass


cli.add_command(fetch)
cli.add_command(latest)
cli.add_command(search)
