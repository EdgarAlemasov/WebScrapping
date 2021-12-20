import requests
import bs4

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}

HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': '_ym_uid=1638286453151056261; _ym_d=1638286453; _ga=GA1.2.1868106554.1638286453; fl=ru; hl=ru; __gads=ID=64d726c86c427ca2:T=1638286456:S=ALNI_MaipUMAhyc5hCNs7wU0Aw659TD82g; feature_streaming_comments=true; visited_articles=301436:531472:480838; _gid=GA1.2.1079399557.1639919261; habr_web_home=ARTICLES_LIST_ALL; _ym_isad=1; _gat=1',
'Host': 'habr.com',
'If-None-Match': 'W/"3a300-brKz58uzNmAEuj/PsbLtYwUdc9w"',
'Referer': 'https://github.com/netology-code/py-homeworks-advanced/tree/master/6.Web-scrapping',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': 'Windows',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

response = requests.get('https://habr.com/ru/all/', headers=HEADERS)
response.raise_for_status()
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')
for article in articles:
    hubs = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
    hubs = set(hub.find('span').text.lower() for hub in hubs)
    titles = article.find('h2', class_='tm-article-snippet__title')
    titles2 = set(title.find('span').text.lower() for title in titles)
    span_title = titles.find('span').text
    preview_text = article.find_all('div', class_='article-formatted-body article-formatted-body_version-2')
    preview_text = set(preview.find('p').text.lower() for preview in preview_text)
    href = article.find('a', class_='tm-article-snippet__title-link')
    data = article.find('span', class_='tm-article-snippet__datetime-published')
    if KEYWORDS & hubs or KEYWORDS & titles2 or KEYWORDS & preview_text:
        data = data.next['title']
        href = href['href']
        url = 'https://habr.com' + href
        print(data, span_title, url)