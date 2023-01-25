import requests
from bs4 import BeautifulSoup


def get_article(url: str):
    """Get Wikipedia article url and scrap article details"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Scrape the article URL
    article_url = response.url

    try:
        # Scrape the title
        title = soup.find("h1").text

        # Scrape the article text
        article = soup.find("div", {"class": "reflist"}).text

        # Scrape the references
        reference = soup.find("ol", {"class": "references"}).text

        # Scrape the last modified date
        last_modified = soup.find("li", {"id": "footer-info-lastmod"}).text
    except AttributeError:
        return

    # Write the results to a JSON file
    data = {
        "article_url": article_url,
        "title": title,
        "article": article,
        "reference": reference,
        "last_modified": last_modified,
    }

    return data
