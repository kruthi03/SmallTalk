#api_utils.py
from gnews import GNews
from newspaper import Article
import re
from googlesearch import search


def get_news(keywords, num_articles=3):
    google_news = GNews()
    articles = google_news.get_news(keywords)[:num_articles]
    news_str = ""
    if articles is not None:
        for article in articles:
            title = article.get("title", "No Title")
            description = article.get("description", "No Description")
            published_date = article.get("published date", "No Description")
            url = article.get("url", "No Description")
            publisher = article.get("description", "No Description")
            news_str += f"- {title}: {description}\n"
        return articles
    else:
        print('no articles found')

#TODO 
def get_pictures(query, **params):
    """
    Fetch and return image URL(s) matching the query.
    """
    pass


def get_urls_from_google(keywords, region = "us", num_results=15, lang="en"):
    results = list(search(keywords, advanced=True, region = region, num_results=num_results, lang=lang))
    return results


def get_articles(urls, max_articles=5):
    articles = []
    for url in urls:
        try:
            art = extract_main_text_from_url(url.url)
            articles.append(art)
        except:
            print('Invalid URL')
        if len(articles) >= max_articles:
            break
    return articles


def extract_main_text_from_url(url: str) -> str:
    if not url or not url.startswith("http"):
        return ""
    try:
        article = Article(url, language='en')
        article.download()
        article.parse()
        text_content = re.sub(r'\n+', '\n', article.text).strip()
        return text_content
    except Exception as e:
        print(f"Failed to extract content from {url}: {e}")
        return ""




