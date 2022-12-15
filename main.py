from scraper import Scrapper
import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()

CALENDAR_PAGE = os.getenv("CALENDAR_PAGE")

class Main(Scrapper):
        
    def main(self):
        years_links = self.get_calendar_years()
        print(len(years_links))

        days_links = self.get_calendar_days(years_links)
        print(len(days_links))

        posts_links = self.get_posts_links(days_links)
        print(len(posts_links))

        for link in posts_links:
            with futures.ThreadPoolExecutor() as executor:
                executor.submit(self.save_post, link)
            
Main(CALENDAR_PAGE).main()




