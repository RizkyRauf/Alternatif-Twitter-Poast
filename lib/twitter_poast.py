import os
import sys
import platform
import time
from datetime import datetime
from selenium import webdriver
from fake_headers import Headers
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import json
from lib.data_extract import DataExtract
from lib.utils import save_to_json
from lib.twitter_replay import TwitterReplay

class TwitterPost:
    """
    Kelas bertanggung jawab untuk berinteraksi dengan pos Twitter.

    Metode:
        configure_browser_options: Mengonfigurasi opsi browser untuk Selenium.
        initialize_driver: Menginisialisasi driver Selenium.
        run_scraper: Menjalankan pengikis Twitter.
    """
    def __init__(self, url: str):
        """
        Inisialisasi TwitterPost dengan URL.

        Args:
            url (str): URL Twitter.
        """
        self.url = url
        self.driver = None

    def configure_browser_options(self) -> webdriver.ChromeOptions:
        """
        Configure browser options for Selenium.

        Returns:
            options (webdriver.ChromeOptions): Browser options for Selenium.
        """
        try:
            # header = Headers().generate()["User-Agent"]
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            # options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-gpu")
            options.add_argument("--log-level=3")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
            return options

        except Exception as e:
            print(f"Error initializing driver: {e}")
            raise
    
    def initialize_driver(self) -> webdriver.Chrome:
        """
        Initialize the Selenium driver.

        Returns:
            driver (webdriver.Chrome): Initialized Selenium driver.
        """
        try:
            # Check user's operating system
            if platform.system() == "Windows":
                chrome_driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../driver/chromedriver.exe"))
            elif platform.system() in ["Linux", "Darwin"]:
                chrome_driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../driver/chromedriver"))

            options = self.configure_browser_options()
            service = ChromeService(executable_path=chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            return driver

        except WebDriverException:
            try:
                print("No Chrome driver available.")
                print("Installing Chrome driver...")
                chromedriver_path = ChromeDriverManager().install()
                chrome_service = ChromeService(executable_path=chromedriver_path)

                print("Initializing Chrome driver...")
                options = self.configure_browser_options()
                driver = webdriver.Chrome(service=chrome_service, options=options)
                return driver
            except Exception as e:
                print(f"Error initializing driver: {e}")
                sys.exit(1)
    
    def run_scraper(self, key: str, start_date: str = None, end_date: str = None):
        """
        Run the scraper.
        
        Args:
            key (str): Keyword pencarian Twitter.
            start_date (str, optional): Tanggal mulai pencarian. Defaults to None.
            end_date (str, optional): Tanggal akhir pencarian. Defaults to None.
        """
        try:
            self.driver = self.initialize_driver()
            self.driver.get(self.url)
            time.sleep(5)
            
            # # Cek apakah ada link Return to Nitter
            # link_element = self.driver.find_element(By.XPATH, "//a[contains(@href,'nitter.poast.org') and contains(text(),'Return to Nitter')]")
            # if link_element:
            #     link_element.click()
            #     print("Return to Nitter.")
                
            # time.sleep(5)
            
            formatted_tweets = []
            while True:
                if start_date and end_date:
                    self.driver.get(f"https://nitter.poast.org/search?f=tweets&q={key}&since={start_date}&until={end_date}&near=")
                    time.sleep(2)
                else:
                    self.driver.get(f"https://nitter.poast.org/search?f=tweets&q={key}")
                    time.sleep(2)
                        
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                tweets = soup.find_all('div', class_='timeline-item')
                    
                if not tweets:
                    print("No tweets found. Scraping finished.")
                    break
                    
                for tweet in tweets:
                    fullname = DataExtract.fullname(tweet)
                    username = DataExtract.username(tweet)
                    text = DataExtract.text(tweet)
                    hashtag = DataExtract.hashtag(text)
                    # Ubah format tanggal menjadi YYYY-MM-DDTHH:MM:SS
                    date = datetime.strptime(DataExtract.date(tweet), "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
                    link = DataExtract.link(tweet)
                    media = DataExtract.media(tweet)
                    stats = DataExtract.stats(tweet)
                    
                    # Jika tidak ada hashtag, tetapkan nilai list kosong
                    if not hashtag:
                        hashtag = []
                    
                    # Perbaiki representasi media
                    if not media['images'] and not media['videos']:
                        media = None
                    
                    # Buat dictionary untuk setiap tweet
                    formatted_tweet = {
                        "type" : "post",
                        "fullname": fullname,
                        "username": username,
                        "text": text,
                        "hashtag": hashtag,
                        "date": date,
                        "link": link,
                        "media": media,
                        "stats": stats
                    }
                    
                    formatted_tweets.append(formatted_tweet)

                print(f"Scraped {len(formatted_tweets)} tweets for {key}")
                    
                try:
                    next_cursor = soup.find('div', class_='show-more').find('a')
                    if next_cursor:
                        next_url = next_cursor['href']
                        self.url = f"https://nitter.poast.org{next_url}"
                        time.sleep(3)
                    else:
                        print("No more next page. Scraping finished.")
                        break
                except AttributeError:
                    print("No more next page. Scraping finished.")
                    break
                
            date_to_json = datetime.now().strftime("%Y-%m-%d")
            save_to_json(formatted_tweets, f"{key}_{date_to_json}.json")

        except Exception as e:
            print(f"Error running scraper: {e}")
            raise

        finally:
            if self.driver:
                self.driver.quit()