import re

from mastodon import Mastodon
import html
import tomd

from config import read_config


def clean_tags(text, tags):
    for tag in tags:
        tag_name = "#" + tag["name"]
        search = "[%s]" % tag_name
        text = text.replace(search, tag_name)
        url = tag["url"]
        search = "(%s)" % url
        text = text.replace(search, "")
    return text


def clean_mentions(text, mentions):
    for mention in mentions:
        username = "@" + mention["username"]
        search = "[%s]" % username
        acct = "@" + mention["acct"]
        text = text.replace(search, acct)
        url = mention["url"]
        search = "(%s)" % url
        text = text.replace(search, "")
    return text


def clean_links(text):
    # Replace [foo](foo) by just foo
    return re.sub(r"\[(.+?)\]\(\1\)", r"\1", text)


def main():
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
    )
    account = mastodon.account_verify_credentials()
    print("Logged in as", account.username)
    for status in mastodon.account_statuses(account.id):
        if status.get("reblog"):
            continue
        as_html = status["content"]
        text = tomd.convert(as_html)
        tags = status["tags"]
        mentions = status["mentions"]
        text = clean_tags(text, tags)
        text = clean_mentions(text, mentions)
        text = text.replace("<br />", "\n")
        text = clean_links(text)
        text = html.unescape(text)
        print("-" * 80)
        print(status["id"], text.strip())
        print()


if __name__ == "__main__":
    main()
