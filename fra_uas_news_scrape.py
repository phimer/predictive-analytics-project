import requests
from bs4 import BeautifulSoup
import re

news_main_page = "https://www.frankfurt-university.de/de/aktuelles/"
url = "https://www.frankfurt-university.de/de/newsmodule/details/mit-projekt-zero-waste-unter-bestplatzierten-beim-data-mining-cup-2023/"


def write_string_to_file(filename, text):
    with open(filename, "w") as file:
        file.write(text)


def remove_special_characters(text):
    return re.sub("[^a-zA-Z0-9 ]", "", text)


def get_all_page_links(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    page2_link = (
        "https://www.frankfurt-university.de"
        + soup.find("a", attrs={"title": "Zu Seite 2"})["href"]
    )
    page3_link = (
        "https://www.frankfurt-university.de"
        + soup.find("a", attrs={"title": "Zu Seite 3"})["href"]
    )

    return [url, page2_link, page3_link]


def get_all_news_links(urls):
    article_links = []

    for url in urls:
        response = requests.get(url)

        if response.status_code == 200:
            content = response.content

            soup = BeautifulSoup(content, "html.parser")

            # get article elementson this page
            article_div = soup.find("div", attrs={"class": "news-simple-list"})
            articles = article_div.find_all("article")

            for article in articles:
                # get article link
                arcticle_link = (
                    article.find("div", attrs={"class": "news-simple-list__text"})
                    .find("div", attrs={"class": "news-simple-list__header"})
                    .find("a", attrs={"class": "news-article-header__link"})
                )

                # add link to article_links list
                article_links.append(
                    "https://www.frankfurt-university.de" + arcticle_link["href"]
                )
        else:
            print("Failed to retrieve webpage.")

    return article_links


def scrape_website_and_save_document_to_file(url):
    response = requests.get(url)

    # Check the status of the request
    if response.status_code == 200:
        content = response.content

        soup = BeautifulSoup(content, "html.parser")

        # 1. headline
        headline = (
            soup.find("div", attrs={"class": "news-article-header"})
            .find_all("h1")[0]
            .text
        )

        # 2. content
        content_div = soup.find("div", attrs={"class": "news-text-wrap"})
        # Get all text within this div
        content_div_text = content_div.get_text()

        # 3. image captions
        try:
            image_captions_text = ""
            image_div = soup.find("div", attrs={"class": "news-img-wrap"})

            for image_caption in image_div.find_all("img"):
                image_captions_text += "\n" + image_caption.get("data-caption")
        except:
            image_captions_text = ""
            print(f"Article has no images: {url}")

        # deprecated
        # h2_elements = content_div.find_all("h2")
        # p_elements = content_div.find_all("p")
        # list_imtems = content_div.find_all("li")
        # text_elements = headline + h2_elements + p_elements
        # for text in text_elements:
        #     if len(document) == 0:
        #         document += text.text
        #     else:
        #         document += "\n" + text.text

        document = headline + "\n" + content_div_text + image_captions_text

        write_string_to_file(
            "documents/"
            + remove_special_characters(document.split("\n", 1)[0])
            + ".txt",
            document,
        )

    else:
        print("Failed to retrieve webpage.")


page_links = get_all_page_links(news_main_page)
news_links = get_all_news_links(page_links)

for news_link in news_links:
    scrape_website_and_save_document_to_file(news_link)
