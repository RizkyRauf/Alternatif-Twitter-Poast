# scraper.py
import time
import unicodedata
from datetime import datetime
from bs4 import BeautifulSoup
from lib.utils import save_to_json
from lib.twitter_poast import TwitterPost
from lib.data_extract import DataExtract

class Scraper:
    """
    Kelas bertanggung jawab untuk mengikis pos Twitter.

    Metode:
        __init__: Menginisialisasi Scraper dengan URL dan jalur berkas kata kunci.
        scrape_tweets: Mengikis tweet berdasarkan kata kunci.
    """
    def __init__(self, url, path_file):
        """
        Menginisialisasi Scraper dengan URL dan jalur berkas kata kunci.

        Args:
            url (str): URL dari pengikis Twitter.
        """
        self.url = url

    def scrape_tweets(self, key):
        """
        Mengikis tweet berdasarkan kata kunci.

        Args:
            key (str): Kata kunci untuk dicari dalam tweet.
        """
        driver = TwitterPost(self.url).initialize_driver()
        driver.get(self.url)
        if driver:
            formatted_tweets = []
            while True:
                driver.get(f"https://nitter.poast.org/search?f=tweets&q={key}")
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                tweets = soup.find_all('div', class_='timeline-item')

                if not tweets:
                    print("No tweets found. Scraping finished.")
                    break

                for tweet in tweets:
                    fullname = DataExtract.fullname(tweet)
                    username = DataExtract.username(tweet)
                    text = DataExtract.text(tweet)
                    hashtag = DataExtract.hashtag(text)
                    date = DataExtract.date(tweet)
                    link = DataExtract.link(tweet)
                    media = DataExtract.media(tweet)
                    stats = DataExtract.stats(tweet)

                    # Create a dictionary for each tweet
                    formatted_tweet = {
                        'fullname': fullname,
                        'username': username,
                        'text': text,
                        'hashtag': hashtag,
                        'date': date,
                        'link': link,
                        'media': media,
                        'stats': stats
                    }
                    formatted_tweets.append(formatted_tweet)

                print(f"Scraped {len(formatted_tweets)} tweets for {key}")

                try:
                    next_cursor = soup.find('div', class_='show-more').find('a')
                    if next_cursor:
                        next_url = next_cursor['href']
                        self.url = f"https://nitter.poast.org{next_url}"
                    else:
                        print("No more next page. Scraping finished.")
                        break
                except AttributeError:
                    print("No more next page. Scraping finished.")
                    break

            date_to_json = datetime.now().strftime("%Y-%m-%d")
            save_to_json(formatted_tweets, f"{key}_{date_to_json}.json")

        driver.quit()