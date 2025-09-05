import requests
from bs4 import BeautifulSoup
import feedparser

# ---------- 1. Росмолодёжь.Гранты (API JSON) ----------
def get_rosmolodezh(limit=10):
    url = f"https://grants.myrosmol.ru/api/v3/contests?limit={limit}&offset=0"
    resp = requests.get(url)
    data = resp.json()
    announcements = []
    for item in data.get("results", []):
        announcements.append({
            "title": item["name"],
            "link": f"https://grants.myrosmol.ru/contests/{item['id']}",
            "deadline": f"{item['date_end_accepting_applications'][:10]}",
            "summary": item.get("description", "")[:200] + "...",
            "source": "Росмолодёжь.Гранты"
        })
    return announcements


# ---------- 2. ФАСИЭ (новости/конкурсы) ----------
def get_fasie_news():
    url = "https://fasie.ru/press/fund-news/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    blocks = soup.select(".news-block")
    announcements = []
    for block in blocks[:10]:
        title = block.select_one("a").text.strip()
        link = block.select_one("a")["href"]
        announcements.append({
            "title": title,
            "link": link,
            "deadline": None,
            "summary": "",
            "source": "ФАСИЭ"
        })
    return announcements


# ---------- 3. Сколково (новости) ----------
def get_skolkovo():
    url = "https://sk.ru/news/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    news_cards = soup.select(".block-materials__item")
    announcements = []
    for card in news_cards[:10]:
        title = card.select_one(".block-materials__title").get_text(strip=True)
        link = "https://sk.ru" + card.select_one("a")["href"]
        announcements.append({
            "title": title,
            "link": link,
            "summary": "",
            "deadline": None,
            "source": "Сколково"
        })
    return announcements


# ---------- 4. GenerationS ----------
def get_generations():
    url = "https://generation-startup.ru/news/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select(".news-item")
    announcements = []
    for item in items[:10]:
        title = item.select_one(".news-item__title").get_text(strip=True)
        link = "https://generation-startup.ru" + item.select_one("a")["href"]
        announcements.append({
            "title": title,
            "link": link,
            "summary": "",
            "deadline": None,
            "source": "GenerationS"
        })
    return announcements


# ---------- 5. Президентские гранты ----------
def get_president_grants():
    url = "https://президентскиегранты.рф/public/application/open"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    contests = soup.select(".contest-page__list-item")
    announcements = []
    for contest in contests:
        title = contest.select_one(".contest-page__list-item-title").get_text(strip=True)
        link_tag = contest.select_one("a")
        link = "https://президентскиегранты.рф" + link_tag["href"] if link_tag else url
        deadline = contest.select_one(".contest-page__list-item-date")
        announcements.append({
            "title": title,
            "link": link,
            "deadline": deadline.get_text(strip=True) if deadline else None,
            "summary": "",
            "source": "Фонд президентских грантов"
        })
    return announcements


# ---------- 6. Московский "Мой бизнес" ----------
def get_moscow_mbm():
    url = "https://mbm.mos.ru/novosti/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    news_cards = soup.select(".b-news__item")
    announcements = []
    for card in news_cards[:10]:
        title = card.select_one(".b-news__title").get_text(strip=True)
        link = "https://mbm.mos.ru" + card.select_one("a")["href"]
        announcements.append({
            "title": title,
            "link": link,
            "summary": card.select_one(".b-news__descr").get_text(strip=True) if card.select_one(".b-news__descr") else "",
            "deadline": None,
            "source": "МБМ Москва"
        })
    return announcements