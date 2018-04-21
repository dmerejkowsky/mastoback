from typing import Generator

from mastodon import Mastodon

from mastoback import Status
from mastoback.config import read_config
import mastoback.store

MAX_TOOTS = 200


def login() -> Mastodon:
    conf = read_config()
    auth_conf = conf["auth"]
    client_id = auth_conf["client_id"]
    client_secret = auth_conf["client_secret"]
    access_token = auth_conf["access_token"]
    url = conf["url"]
    mastodon = Mastodon(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        api_base_url=url,
        ratelimit_method='throw',
    )
    return mastodon


def yield_statuses(mastodon: Mastodon, account_id: int, *,
                   since_id: int,
                   limit: int = 200) -> Generator[Status, None, None]:
    statuses = mastodon.account_statuses(account_id, limit=MAX_TOOTS, since_id=since_id)
    yield from statuses
    while statuses:
        statuses = mastodon.fetch_next(statuses)
        if statuses:
            yield from statuses


def main() -> None:
    mastodon = login()
    account = mastodon.account_verify_credentials()
    print("Logged in as", account.username)
    store = mastoback.store.Store()
    latest_id = store.get_latest_id()
    i = 0
    for status in yield_statuses(mastodon, account.id, since_id=latest_id, limit=200):
        toot = mastoback.toot_from_status(status)
        store.add_toot(toot)
        i += 1
    if i:
        print("Stored", i, "new toots")
    else:
        print("No new toots")


if __name__ == "__main__":
    main()
