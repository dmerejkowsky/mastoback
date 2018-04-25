# mastoback

Searchable backup of mastodon toots

# Requiremnts

Python **3.6** or higher

MongoDB 

# Setup

* Run the `register_app` and `gen_token` scripts
* Create a `~/.config/mastoback.yml` looking like:

```yaml
# your mastodon instance
url: "https://mamot.fr"

auth:
  # generated by the aforementioned scripts.
  client_id: ...
  client_secret: ...
  access_token: ...

# Use for search
index_path: /some/writeable/path
```

# Usage

Run `mastodback fetch` to fetch your latest toots.

Use `mastoback search <query>` to display matching toots.

```
$ mastoback search links
Found 10 results
--------------------------------------------------------------------------------
New link added to https://dmerej.info/blog/pages/links/
Daplie: https://daplie.com/
https://mamot.fr/@dmerej/98947577777033562

--------------------------------------------------------------------------------
New link added to https://dmerej.info/blog/pages/links/
js2js: https://eleks.github.io/js2js/
https://mamot.fr/@dmerej/3066566
```

# FAQ

* Why ?

Because I can.

* Why mongodb ?

I'm lazy and I wanted to store the whole data returned by the Mastodon API "just in case". Mongo is nice for this.

* Why Python 3.6 only ?

Because I wanted to play with mypy and I prefer type annotations to `# type:` comments

* What's next ?

Nothing. I have no plan on adding features to this project, I just wanted a searchable backup from the command line.

I could spend more time on the conversion from html to text maybe, but apart from that I consider this project done.

