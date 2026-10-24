#!/usr/bin/env python3
"""Génère feed.xml à partir des fichiers posts/*.html.

Sans dépendance. À relancer après chaque nouveau post :
    python3 tools/build-feed.py

Le flux porte le contenu complet dans <content:encoded>, ce qui permet à dev.to
de créer un brouillon utilisable à l'import, avec canonical_url déjà pointé ici.
"""
import glob
import html
import os
import re
from datetime import datetime, timezone
from email.utils import format_datetime

SITE = "https://wistonlestin.com"
TITLE = "Wiston Lestin — Detection engineering & AI security"
DESC = "Detection engineering, detection-as-code and AI security. Lab write-ups and field notes."
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def absolutize(body: str) -> str:
    """Les liens relatifs n'ont pas de sens hors du site : les rendre absolus."""
    body = re.sub(r'href="/(?!/)', f'href="{SITE}/', body)
    return re.sub(r'src="/(?!/)', f'src="{SITE}/', body)

def read_post(path: str):
    raw = open(path, encoding="utf-8").read()
    flat = raw.replace("\n", " ")

    m = re.search(r"<title>(.*?)</title>", flat)
    title = html.unescape(m.group(1)).strip() if m else None

    m = re.search(r'name="description"\s+content="(.*?)"', flat)
    desc = html.unescape(m.group(1)).strip() if m else ""

    m = re.search(r'<p class="meta mono">\s*(\d{4})-(\d{2})-(\d{2})', flat)
    if not (title and m):
        return None
    date = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), 12, 0, tzinfo=timezone.utc)

    # corps = ce qui suit la ligne de méta, jusqu'à la fin de l'article
    body = ""
    b = re.search(r'<p class="meta mono">.*?</p>(.*?)</article>', raw, re.S)
    if b:
        body = absolutize(b.group(1)).strip()

    slug = os.path.basename(path)[:-5]
    return {
        "title": title,
        "desc": desc,
        "date": date,
        "url": f"{SITE}/posts/{slug}",   # URL canonique, sans extension
        "body": body,
    }

def main():
    posts = [p for p in (read_post(f) for f in glob.glob(os.path.join(ROOT, "posts", "*.html"))) if p]
    posts.sort(key=lambda p: p["date"], reverse=True)

    items = []
    for p in posts:
        items.append(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{p['url']}</link>
      <guid isPermaLink="true">{p['url']}</guid>
      <pubDate>{format_datetime(p['date'])}</pubDate>
      <description>{html.escape(p['desc'])}</description>
      <content:encoded><![CDATA[{p['body']}]]></content:encoded>
    </item>""")

    built = format_datetime(posts[0]["date"]) if posts else format_datetime(datetime.now(timezone.utc))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{html.escape(TITLE)}</title>
    <link>{SITE}/</link>
    <description>{html.escape(DESC)}</description>
    <language>en</language>
    <lastBuildDate>{built}</lastBuildDate>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
"""
    out = os.path.join(ROOT, "feed.xml")
    open(out, "w", encoding="utf-8").write(feed)
    print(f"feed.xml : {len(posts)} billets, le plus récent {posts[0]['date'].date()}")

if __name__ == "__main__":
    main()
