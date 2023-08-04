import requests
from bs4 import BeautifulSoup
import re


class StudiengangScraper:
    def __init__(self):
        self.main_url = ""
        self.studiengang_urls = []

    def set_main_url(self, url):
        self.main_url = url

    def get_all_studiengaenge(self):
        if self.main_url == "":
            raise Exception("main_url not set")

        content = requests.get(self.main_url).content

        soup = BeautifulSoup(content, "html.parser")

        bachelor_programs_div = soup.find("div", attrs={"id": "tab-91863"})

        bachelor_programs = bachelor_programs_div.find_all("li")

        for bachelor_program in bachelor_programs:
            link = bachelor_program.find("a")
            if link is not None:
                self.studiengang_urls.append(
                    "https://www.frankfurt-university.de" + link.get("href")
                )

    def write_string_to_file(self, filename, text):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"File {filename} written successfully")

    def _scrape_studiengang(self, studiengang_url):
        content = requests.get(studiengang_url).content
        soup = BeautifulSoup(content, "html.parser")

        studiengang_main_content_div = soup.find("div", attrs={"id": "main-content"})
        studiengang_main_content = studiengang_main_content_div.get_text()

        self.write_string_to_file(
            "studiengaenge/"
            + StudiengangScraper._get_name_from_url(studiengang_url)
            + ".txt",
            studiengang_main_content,
        )

    def scrape_studiengaenge(self):
        for studiengang_url in self.studiengang_urls:
            self._scrape_studiengang(studiengang_url)

    def print_all_studiengaenge_urls(self):
        for studiengang_url in self.studiengang_urls:
            print(studiengang_url)

    def remove_special_characters(text):
        return re.sub("[^a-zA-Z0-9 ]", "", text)

    def _get_name_from_url(url):
        # Split the remaining string on '-studiengange/'
        parts = url.split("-studiengange/")
        # print(f"parts: {parts}")
        text = parts[1].replace("/", "-")

        return text
