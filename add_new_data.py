import datetime

import requests


def get_header(date):
    return f"""
<!DOCTYPE html>
  <html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>{date} 時点 ニコニコ動画 累計再生数ランキング</title>
  </head>
  <body>
    <header>
      <h2>{date} 時点 <a href="https://www.nicovideo.jp/video_top">ニコニコ動画</a> 累計再生数ランキング</h2>
    </header>
    <ui>
      <li>毎日、日本時間の午前 6 時頃に更新</li>
      <li>検索で出てこない動画 (いわゆる再生数工作動画など) は除外</li>
      <li><a href="../index.html">他の日のランキング</a></li>
    </ui>
    <p>"""


def get_footer():
    return """
    </p>
  </body>
</html>"""


def get_ranking_data():
    # APIのエンドポイントと必要なパラメータ
    api_url = "https://snapshot.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
    params = {
        "q": "",
        "targets": "title",
        "fields": "title,contentId,viewCounter",
        "_sort": "-viewCounter",
        "_limit": 100,
    }

    response = requests.get(api_url, params=params)
    print(response)

    js = response.json()
    print(js)

    return js["data"]


def get_video_html(rank, title, vid, viewcount):
    return f"""
      {rank} 位 {viewcount:,} 再生<br />
      <iframe width="550" height="120" src="https://ext.nicovideo.jp/thumb/{vid}" scrolling="no" style="border: solid 1px #ccc" frameborder="0"
      ><a href="https://www.nicovideo.jp/watch/{vid}">{title}</a></iframe><br />"""


jst = datetime.timezone(datetime.timedelta(hours=9), "JST")  # 日本時間は UTC から +9 時間
date_today = str(datetime.datetime.now(jst).date())  # yyyy-mm-dd
print("date_today:", date_today)

print("get_ranking_data start")
ranking_data = get_ranking_data()
print("get_ranking_data end")

print("write new html file start")
with open(f"data/{date_today.replace('-','')}.html", "w", encoding="utf-8") as f:
    f.write(get_header(date_today))
    for i, video in enumerate(ranking_data):
        print(i + 1, video["title"], video["contentId"], video["viewCounter"])
        f.write(get_video_html(i + 1, video["title"], video["contentId"], video["viewCounter"]))
    f.write(get_footer())
print("write new html file end")


new_link = f"""      <a href="data/{date_today.replace("-","")}.html">{date_today}</a><br />"""
target = "<!-- ここに追加 -->"

print("replace index.html start")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html.replace(target, target + "\n" + new_link))
print("replace index.html end")
