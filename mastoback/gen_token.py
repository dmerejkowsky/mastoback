from mastodon import Mastodon

mastodon = Mastodon(
    client_id="mastoback.secret",
    api_base_url="<url>"
)

mastodon.log_in(
    'user',
    'p4ssw0rd',
    to_file='token'
)
