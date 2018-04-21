from mastodon import Mastodon

mastodon = Mastodon.create_app(
   "mastoback",
   api_base_url="<url>",
   to_file="mastoback.secret"
)
