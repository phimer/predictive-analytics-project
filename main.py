from StudiengangScraper import StudiengangScraper


studiengangScraper = StudiengangScraper()
studiengangScraper.set_main_url("https://www.frankfurt-university.de/de/studium/")
studiengangScraper.get_all_studiengaenge()
studiengangScraper.print_all_studiengaenge_urls()

# studiengangScraper._scrape_studiengang_test(studiengang_index=22)
studiengangScraper.scrape_studiengaenge()
