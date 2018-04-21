import re
from typing import Any, Dict, List, NewType

import tomd
import html


# Status is what get returns by the rest API
Status = NewType('Status', Dict[str, Any])
Tag = NewType('Tag', Dict[str, str])
Mention = NewType('Mention', Dict[str, str])


def clean_tags(text: str, tags: List[Tag]) -> str:
    for tag in tags:
        tag_name = "#" + tag["name"]
        search = "[%s]" % tag_name
        text = text.replace(search, tag_name)
        url = tag["url"]
        search = "(%s)" % url
        text = text.replace(search, "")
    return text


def clean_mentions(text: str, mentions: List[Mention]) -> str:
    for mention in mentions:
        username = "@" + mention["username"]
        search = "[%s]" % username
        acct = "@" + mention["acct"]
        text = text.replace(search, acct)
        url = mention["url"]
        search = "(%s)" % url
        text = text.replace(search, "")
    return text


def clean_links(text: str) -> str:
    # Replace [foo](foo) by just foo
    return re.sub(r"\[(.+?)\]\(\1\)", r"\1", text)


def extract_text(status: Status) -> str:
    as_html = status["content"]
    text: str = tomd.convert(as_html)
    tags = status["tags"]
    mentions = status["mentions"]
    text = clean_tags(text, tags)
    text = clean_mentions(text, mentions)
    text = text.replace("<br />", "\n")
    text = clean_links(text)
    text = html.unescape(text)
    return text


class Toot:
    def __init__(self, toot_id: int, text: str, url: str, status: Status) -> None:
        self.status = status
        self.text = text
        self.id = toot_id
        self.url = url


def toot_from_status(status: Status) -> Toot:
    text = extract_text(status)
    status_id = status["id"]
    url = status["url"]
    return Toot(status_id, text, url, status)
