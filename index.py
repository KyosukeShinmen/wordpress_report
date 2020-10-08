from module import connect
from module import urlcollection as uc
from module import sh
from module import ga
from module import sc
from bs4 import BeautifulSoup as bs
from datetime import datetime, date, timedelta
from tqdm import tqdm

fieldnames = ['id', 'title', 'url', 'thumbnail', 'PV', 'lead', 'text length', 'internal link', 'images', 'post date', 'last updated', "query"]
mysql = connect.mysql()
items = mysql.getPost("post")
rows = []
pv_summary = ga.main()
rank_summary = sc.googleSC().getQuery()

for item in tqdm(items):
    post_id = item['ID']
    content = item['post_content'].decode("utf-8")
    soup = bs(content, "html.parser")

    links = [uc.absolutePath(x.get("href")) if x.get("href") is not None else "" for x in soup.find_all("a")]
    text = soup.get_text().replace("\n", "").replace("\r", "")
    images = [uc.absolutePath(x.get("src")) if x.get("src") is not None else "" for x in soup.find_all("img")]
    thumbnail = mysql.select(f"SELECT guid FROM {mysql.prefix}_posts WHERE ID = (SELECT meta_value FROM {mysql.prefix}_postmeta WHERE post_id = {post_id} AND meta_key = '_thumbnail_id');")
    if len(thumbnail) != 0:
        thumb = thumbnail[0]['guid'].decode("utf-8")
    else:
        thumb = "-"

    permalink = uc.getRedirectUrl(uc.createUrlFromPostId(post_id))
    root_path = permalink.replace(uc.domain(), "")

    if root_path in pv_summary:
        page_view = pv_summary[root_path]
    else:
        page_view = "-"

    if permalink in rank_summary:
        query = rank_summary[permalink]
    else:
        query = None

    row = {"id": post_id,
            "title": item['post_title'].decode("utf-8"),
            "url": permalink,
            "thumbnail": thumb,
            "PV": page_view,
            "lead": text[0:300],
            "text length": len(text),
            "internal link": "\n".join(links),
            "images": "\n".join(images),
            "post date": item["post_date"].strftime('%Y/%m/%d'),
            "last updated": item["post_modified"].strftime('%Y/%m/%d'),
            "query": query
    }
    
    rows.append([x for x in row.values()])

today = datetime.today()
sh.Spread().createReport(datetime.strftime(today - timedelta(days=1), '%Y-%m-%d'), rows, [fieldnames])