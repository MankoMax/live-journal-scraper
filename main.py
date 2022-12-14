from scraper import Scrapper
import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()

CALENDAR_PAGE = os.getenv("CALENDAR_PAGE")
TEST_LINKS = ["https://navalny.livejournal.com/209488.html", "https://navalny.livejournal.com/209963.html", "https://navalny.livejournal.com/616157.html"]


class Main(Scrapper):
        
    def main(self):
        years_links = self.get_calendar_years()
        print(len(years_links))

        days_links = self.get_calendar_days(years_links)
        print(len(days_links))

        posts_links = self.get_posts_links(days_links)
        print(len(posts_links))

        for link in TEST_LINKS:
            self.save_post(link)
            
Main(CALENDAR_PAGE).main()




